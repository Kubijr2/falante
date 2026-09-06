from app.core.current_user import get_current_user
from app.main import app


def _as_user(user):
    """Temporarily makes `client` authenticate as a specific user for one request block."""
    app.dependency_overrides[get_current_user] = lambda: user


def _restore_default_user(test_user):
    app.dependency_overrides[get_current_user] = lambda: test_user


def test_users_have_separate_vocabulary_lists(client, test_user, second_user):
    _as_user(test_user)
    client.post("/api/v1/vocabulary", json={"portuguese": "falar", "english": "to speak", "tags": []})

    _as_user(second_user)
    client.post("/api/v1/vocabulary", json={"portuguese": "comer", "english": "to eat", "tags": []})

    response = client.get("/api/v1/vocabulary")
    words = [w["portuguese"] for w in response.json()]
    assert words == ["comer"]  # only second_user's word, not test_user's

    _as_user(test_user)
    response = client.get("/api/v1/vocabulary")
    words = [w["portuguese"] for w in response.json()]
    assert words == ["falar"]

    _restore_default_user(test_user)


def test_user_cannot_fetch_another_users_vocabulary_by_id(client, test_user, second_user):
    _as_user(test_user)
    created = client.post(
        "/api/v1/vocabulary", json={"portuguese": "falar", "english": "to speak", "tags": []}
    ).json()

    _as_user(second_user)
    response = client.get(f"/api/v1/vocabulary/{created['id']}")
    assert response.status_code == 404  # not 403 — doesn't reveal that the id exists at all

    _restore_default_user(test_user)


def test_user_cannot_delete_another_users_vocabulary(client, test_user, second_user):
    _as_user(test_user)
    created = client.post(
        "/api/v1/vocabulary", json={"portuguese": "falar", "english": "to speak", "tags": []}
    ).json()

    _as_user(second_user)
    delete_response = client.delete(f"/api/v1/vocabulary/{created['id']}")
    assert delete_response.status_code == 404

    _as_user(test_user)
    get_response = client.get(f"/api/v1/vocabulary/{created['id']}")
    assert get_response.status_code == 200  # still there — the delete attempt had no effect

    _restore_default_user(test_user)


def test_dashboard_stats_are_isolated_per_user(client, test_user, second_user):
    _as_user(test_user)
    word = client.post(
        "/api/v1/vocabulary", json={"portuguese": "falar", "english": "to speak", "tags": []}
    ).json()
    client.post(f"/api/v1/flashcards/{word['id']}/review", json={"result": "easy"})

    _as_user(second_user)
    response = client.get("/api/v1/dashboard/summary")
    body = response.json()
    assert body["total_words"] == 0
    assert body["total_reviews"] == 0

    _as_user(test_user)
    response = client.get("/api/v1/dashboard/summary")
    body = response.json()
    assert body["total_words"] == 1
    assert body["total_reviews"] == 1

    _restore_default_user(test_user)


def test_writing_history_is_isolated_per_user(client, db_session, test_user, second_user):
    import json as jsonlib

    from app.api.v1 import writing
    from app.repositories.writing_repository import WritingSubmissionRepository
    from app.services.ai.base import AIProvider, ChatMessage
    from app.services.writing_coach_service import WritingCoachService

    valid_response = jsonlib.dumps(
        {"overall_feedback": "Good.", "corrections": [], "vocabulary_suggestions": []}
    )

    class FakeProvider(AIProvider):
        def generate_reply(self, messages: list[ChatMessage], json_mode: bool = False) -> str:
            return valid_response

    def make_service_for(user):
        return lambda: WritingCoachService(
            WritingSubmissionRepository(db_session, user.id), provider_factory=lambda: FakeProvider()
        )

    _as_user(test_user)
    app.dependency_overrides[writing.get_service] = make_service_for(test_user)
    client.post("/api/v1/writing/review", json={"text": "Eu gosto de café."})

    _as_user(second_user)
    app.dependency_overrides[writing.get_service] = make_service_for(second_user)
    response = client.get("/api/v1/writing")
    assert response.json() == []

    _restore_default_user(test_user)
    app.dependency_overrides.pop(writing.get_service, None)


def test_grammar_and_verbs_stay_public_and_shared(client, test_user, second_user):
    # Sanity check that the public routers were NOT accidentally scoped —
    # both users should see the exact same shared reference content.
    _as_user(test_user)
    grammar_a = client.get("/api/v1/grammar").json()
    verbs_a = client.get("/api/v1/verbs").json()

    _as_user(second_user)
    grammar_b = client.get("/api/v1/grammar").json()
    verbs_b = client.get("/api/v1/verbs").json()

    assert grammar_a == grammar_b
    assert len(verbs_a) == len(verbs_b) == 85

    _restore_default_user(test_user)
