import json

from app.api.v1 import writing
from app.main import app
from app.repositories.writing_repository import WritingSubmissionRepository
from app.services.ai.base import AIProvider, ChatMessage
from app.services.ai.factory import AIFeatureDisabledError
from app.services.writing_coach_service import WritingCoachService

VALID_RESPONSE = json.dumps(
    {
        "overall_feedback": "Good effort overall.",
        "corrections": [
            {
                "type": "grammar",
                "original": "Eu gosta",
                "corrected": "Eu gosto",
                "explanation": "First person conjugation.",
            }
        ],
        "vocabulary_suggestions": [
            {"portuguese": "com certeza", "english": "for sure", "reason": "Common filler phrase."}
        ],
    }
)


class FakeProvider(AIProvider):
    def __init__(self, reply: str = VALID_RESPONSE):
        self.reply = reply

    def generate_reply(self, messages: list[ChatMessage], json_mode: bool = False) -> str:
        return self.reply


def _override_with_fake(db_session, reply: str = VALID_RESPONSE):
    def override_service():
        return WritingCoachService(
            WritingSubmissionRepository(db_session), provider_factory=lambda: FakeProvider(reply)
        )

    app.dependency_overrides[writing.get_service] = override_service


def test_review_endpoint_returns_structured_result(client, db_session):
    _override_with_fake(db_session)
    try:
        response = client.post("/api/v1/writing/review", json={"text": "Eu gosta de café."})
        assert response.status_code == 201
        body = response.json()
        assert body["overall_feedback"] == "Good effort overall."
        assert body["corrections"][0]["original"] == "Eu gosta"
        assert body["vocabulary_suggestions"][0]["portuguese"] == "com certeza"
        assert "id" in body
        assert "created_at" in body
    finally:
        app.dependency_overrides.pop(writing.get_service, None)


def test_review_endpoint_rejects_empty_text(client):
    response = client.post("/api/v1/writing/review", json={"text": ""})
    assert response.status_code == 422


def test_review_endpoint_503_when_ai_disabled(client, db_session):
    def raise_disabled():
        raise AIFeatureDisabledError("not configured")

    def override_service():
        return WritingCoachService(WritingSubmissionRepository(db_session), provider_factory=raise_disabled)

    app.dependency_overrides[writing.get_service] = override_service
    try:
        response = client.post("/api/v1/writing/review", json={"text": "Some text"})
        assert response.status_code == 503
    finally:
        app.dependency_overrides.pop(writing.get_service, None)


def test_review_endpoint_502_on_malformed_ai_response(client, db_session):
    _override_with_fake(db_session, reply="not valid json")
    try:
        response = client.post("/api/v1/writing/review", json={"text": "Some text"})
        assert response.status_code == 502
    finally:
        app.dependency_overrides.pop(writing.get_service, None)


def test_list_and_get_submission(client, db_session):
    _override_with_fake(db_session)
    try:
        create_response = client.post("/api/v1/writing/review", json={"text": "Eu gosta de café."})
        submission_id = create_response.json()["id"]

        list_response = client.get("/api/v1/writing")
        assert list_response.status_code == 200
        assert len(list_response.json()) == 1

        detail_response = client.get(f"/api/v1/writing/{submission_id}")
        assert detail_response.status_code == 200
        assert detail_response.json()["id"] == submission_id
    finally:
        app.dependency_overrides.pop(writing.get_service, None)


def test_get_missing_submission_returns_404(client):
    response = client.get("/api/v1/writing/999")
    assert response.status_code == 404
