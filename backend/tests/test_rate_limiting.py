import pytest

from app.core.rate_limit import limiter


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    """
    The limiter's counters are in-memory and persist for the lifetime of
    the process — without resetting between tests, whichever test runs
    first would "use up" quota that later tests then find already
    exhausted. Runs before AND after every test in this file.
    """
    limiter.reset()
    yield
    limiter.reset()


def test_tutor_ask_allows_requests_under_the_limit(client, db_session, monkeypatch):
    from app.api.v1 import tutor
    from app.main import app
    from app.repositories.grammar_repository import GrammarRepository
    from app.services.ai.base import AIProvider, ChatMessage
    from app.services.tutor_service import TutorService
    from app.core.config import settings

    monkeypatch.setattr(settings, "ai_rate_limit_per_day", 2)

    class FakeProvider(AIProvider):
        def generate_reply(self, messages: list[ChatMessage], json_mode: bool = False) -> str:
            return "answer"

    app.dependency_overrides[tutor.get_service] = lambda: TutorService(
        GrammarRepository(db_session), provider_factory=lambda: FakeProvider()
    )
    try:
        for _ in range(2):
            response = client.post(
                "/api/v1/tutor/ask", json={"question": "Why?", "topic_slug": None, "history": []}
            )
            assert response.status_code == 200
    finally:
        app.dependency_overrides.pop(tutor.get_service, None)


def test_tutor_ask_blocks_requests_over_the_limit(client, db_session, monkeypatch):
    from app.api.v1 import tutor
    from app.main import app
    from app.repositories.grammar_repository import GrammarRepository
    from app.services.ai.base import AIProvider, ChatMessage
    from app.services.tutor_service import TutorService
    from app.core.config import settings

    monkeypatch.setattr(settings, "ai_rate_limit_per_day", 1)

    class FakeProvider(AIProvider):
        def generate_reply(self, messages: list[ChatMessage], json_mode: bool = False) -> str:
            return "answer"

    app.dependency_overrides[tutor.get_service] = lambda: TutorService(
        GrammarRepository(db_session), provider_factory=lambda: FakeProvider()
    )
    try:
        first = client.post(
            "/api/v1/tutor/ask", json={"question": "Why?", "topic_slug": None, "history": []}
        )
        assert first.status_code == 200

        second = client.post(
            "/api/v1/tutor/ask", json={"question": "Why again?", "topic_slug": None, "history": []}
        )
        assert second.status_code == 429
        assert "daily limit" in second.json()["detail"].lower() or "reached today's limit" in second.json()["detail"].lower()
    finally:
        app.dependency_overrides.pop(tutor.get_service, None)


def test_writing_review_is_also_rate_limited(client, db_session, monkeypatch):
    import json as jsonlib

    from app.api.v1 import writing
    from app.main import app
    from app.repositories.writing_repository import WritingSubmissionRepository
    from app.services.ai.base import AIProvider, ChatMessage
    from app.services.writing_coach_service import WritingCoachService
    from app.core.config import settings

    monkeypatch.setattr(settings, "ai_rate_limit_per_day", 1)

    valid_response = jsonlib.dumps(
        {"overall_feedback": "Good.", "corrections": [], "vocabulary_suggestions": []}
    )

    class FakeProvider(AIProvider):
        def generate_reply(self, messages: list[ChatMessage], json_mode: bool = False) -> str:
            return valid_response

    app.dependency_overrides[writing.get_service] = lambda: WritingCoachService(
        WritingSubmissionRepository(db_session), provider_factory=lambda: FakeProvider()
    )
    try:
        first = client.post("/api/v1/writing/review", json={"text": "Eu gosto de café."})
        assert first.status_code == 201

        second = client.post("/api/v1/writing/review", json={"text": "Outro texto."})
        assert second.status_code == 429
    finally:
        app.dependency_overrides.pop(writing.get_service, None)


def test_rate_limit_does_not_apply_to_non_ai_endpoints(client, monkeypatch):
    from app.core.config import settings

    monkeypatch.setattr(settings, "ai_rate_limit_per_day", 1)
    # Ordinary CRUD endpoints should never be throttled by the AI rate
    # limit — hit vocabulary far more than the AI limit and confirm it's
    # unaffected.
    for _ in range(5):
        response = client.get("/api/v1/vocabulary")
        assert response.status_code == 200
