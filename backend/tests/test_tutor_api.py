from app.api.v1 import tutor
from app.core.config import settings
from app.main import app
from app.repositories.grammar_repository import GrammarRepository
from app.services.ai.base import AIProvider, ChatMessage
from app.services.ai.factory import AIFeatureDisabledError
from app.services.tutor_service import TutorService


class FakeProvider(AIProvider):
    def generate_reply(self, messages: list[ChatMessage]) -> str:
        return "Fake AI reply."


def test_status_reflects_missing_api_key(client, monkeypatch):
    monkeypatch.setattr(settings, "ai_api_key", None)
    response = client.get("/api/v1/tutor/status")
    assert response.status_code == 200
    assert response.json() == {"enabled": False}


def test_status_reflects_configured_api_key(client, monkeypatch):
    monkeypatch.setattr(settings, "ai_api_key", "fake-key")
    response = client.get("/api/v1/tutor/status")
    assert response.json() == {"enabled": True}


def test_ask_returns_answer_when_configured(client, db_session):
    def override_service():
        return TutorService(GrammarRepository(db_session), provider_factory=lambda: FakeProvider())

    app.dependency_overrides[tutor.get_service] = override_service
    try:
        response = client.post(
            "/api/v1/tutor/ask",
            json={"question": "Why ser?", "topic_slug": None, "history": []},
        )
        assert response.status_code == 200
        assert response.json() == {"answer": "Fake AI reply."}
    finally:
        app.dependency_overrides.pop(tutor.get_service, None)


def test_ask_returns_503_when_ai_disabled(client, db_session):
    def raise_disabled():
        raise AIFeatureDisabledError("not configured")

    def override_service():
        return TutorService(GrammarRepository(db_session), provider_factory=raise_disabled)

    app.dependency_overrides[tutor.get_service] = override_service
    try:
        response = client.post(
            "/api/v1/tutor/ask",
            json={"question": "Why ser?", "topic_slug": None, "history": []},
        )
        assert response.status_code == 503
        assert "not configured" in response.json()["detail"]
    finally:
        app.dependency_overrides.pop(tutor.get_service, None)


def test_ask_rejects_empty_question(client):
    response = client.post(
        "/api/v1/tutor/ask", json={"question": "", "topic_slug": None, "history": []}
    )
    assert response.status_code == 422
