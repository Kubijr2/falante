import pytest


def test_study_assistant_requires_auth():
    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app) as unauthenticated_client:
        response = unauthenticated_client.get("/api/v1/study-assistant")
        assert response.status_code == 401


def test_get_history_starts_empty(client):
    response = client.get("/api/v1/study-assistant")
    assert response.status_code == 200
    assert response.json() == []


def test_send_message_returns_503_when_ai_disabled(client, monkeypatch):
    # Force the disabled state explicitly rather than relying on whatever
    # AI_API_KEY happens to be set in this environment's .env — the other
    # AI endpoints' tests (test_tutor_api.py) follow the same convention.
    from app.core.config import settings

    monkeypatch.setattr(settings, "ai_api_key", None)
    response = client.post("/api/v1/study-assistant/message", json={"message": "hi"})
    assert response.status_code == 503


def test_send_message_with_a_fake_provider_saves_history(client, db_session, test_user):
    from app.api.v1 import study_assistant
    from app.main import app
    from app.repositories.study_assistant_repository import StudyAssistantRepository
    from app.repositories.vocabulary_repository import VocabularyRepository
    from app.services.ai.base import AIProvider, ChatMessage
    from app.services.study_assistant_service import StudyAssistantService

    class FakeProvider(AIProvider):
        def generate_reply(self, messages, json_mode=False):
            return "Let's practice together!"

    app.dependency_overrides[study_assistant.get_service] = lambda: StudyAssistantService(
        StudyAssistantRepository(db_session, test_user.id),
        VocabularyRepository(db_session, test_user.id),
        provider_factory=lambda: FakeProvider(),
    )
    try:
        response = client.post("/api/v1/study-assistant/message", json={"message": "Hi there"})
        assert response.status_code == 200
        assert response.json()["reply"] == "Let's practice together!"

        history = client.get("/api/v1/study-assistant").json()
        assert len(history) == 2
        assert history[0]["role"] == "user"
        assert history[0]["content"] == "Hi there"
        assert history[1]["role"] == "assistant"
    finally:
        app.dependency_overrides.pop(study_assistant.get_service, None)


def test_clear_history(client, db_session, test_user):
    from app.api.v1 import study_assistant
    from app.main import app
    from app.repositories.study_assistant_repository import StudyAssistantRepository
    from app.repositories.vocabulary_repository import VocabularyRepository
    from app.services.ai.base import AIProvider
    from app.services.study_assistant_service import StudyAssistantService

    class FakeProvider(AIProvider):
        def generate_reply(self, messages, json_mode=False):
            return "reply"

    app.dependency_overrides[study_assistant.get_service] = lambda: StudyAssistantService(
        StudyAssistantRepository(db_session, test_user.id),
        VocabularyRepository(db_session, test_user.id),
        provider_factory=lambda: FakeProvider(),
    )
    try:
        client.post("/api/v1/study-assistant/message", json={"message": "hi"})
        assert len(client.get("/api/v1/study-assistant").json()) == 2

        delete_response = client.delete("/api/v1/study-assistant")
        assert delete_response.status_code == 204
        assert client.get("/api/v1/study-assistant").json() == []
    finally:
        app.dependency_overrides.pop(study_assistant.get_service, None)


def test_conversation_history_is_isolated_per_user(client, db_session, test_user, second_user):
    from app.api.v1 import study_assistant
    from app.core.current_user import get_current_user
    from app.main import app
    from app.repositories.study_assistant_repository import StudyAssistantRepository
    from app.repositories.vocabulary_repository import VocabularyRepository
    from app.services.ai.base import AIProvider
    from app.services.study_assistant_service import StudyAssistantService

    class FakeProvider(AIProvider):
        def generate_reply(self, messages, json_mode=False):
            return "reply"

    def service_for(user):
        return lambda: StudyAssistantService(
            StudyAssistantRepository(db_session, user.id),
            VocabularyRepository(db_session, user.id),
            provider_factory=lambda: FakeProvider(),
        )

    app.dependency_overrides[get_current_user] = lambda: test_user
    app.dependency_overrides[study_assistant.get_service] = service_for(test_user)
    client.post("/api/v1/study-assistant/message", json={"message": "test_user's message"})

    app.dependency_overrides[get_current_user] = lambda: second_user
    app.dependency_overrides[study_assistant.get_service] = service_for(second_user)
    response = client.get("/api/v1/study-assistant")
    assert response.json() == []

    app.dependency_overrides[get_current_user] = lambda: test_user
    app.dependency_overrides.pop(study_assistant.get_service, None)


def test_rate_limit_applies_to_message_endpoint(client, db_session, test_user, monkeypatch):
    from app.api.v1 import study_assistant
    from app.core.config import settings
    from app.core.rate_limit import limiter
    from app.main import app
    from app.repositories.study_assistant_repository import StudyAssistantRepository
    from app.repositories.vocabulary_repository import VocabularyRepository
    from app.services.ai.base import AIProvider
    from app.services.study_assistant_service import StudyAssistantService

    limiter.reset()
    monkeypatch.setattr(settings, "ai_rate_limit_per_day", 1)

    class FakeProvider(AIProvider):
        def generate_reply(self, messages, json_mode=False):
            return "reply"

    app.dependency_overrides[study_assistant.get_service] = lambda: StudyAssistantService(
        StudyAssistantRepository(db_session, test_user.id),
        VocabularyRepository(db_session, test_user.id),
        provider_factory=lambda: FakeProvider(),
    )
    try:
        first = client.post("/api/v1/study-assistant/message", json={"message": "one"})
        assert first.status_code == 200

        second = client.post("/api/v1/study-assistant/message", json={"message": "two"})
        assert second.status_code == 429
    finally:
        app.dependency_overrides.pop(study_assistant.get_service, None)
        limiter.reset()
