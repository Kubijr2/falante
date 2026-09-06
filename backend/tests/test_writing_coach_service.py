import json

import pytest

from app.repositories.writing_repository import WritingSubmissionRepository
from app.services.ai.base import AIProvider, ChatMessage
from app.services.ai.factory import AIFeatureDisabledError
from app.services.writing_coach_service import AIResponseParseError, WritingCoachService

VALID_RESPONSE = json.dumps(
    {
        "overall_feedback": "Nice work — mostly natural, a couple of small fixes below.",
        "corrections": [
            {
                "type": "grammar",
                "original": "Eu gosta de café",
                "corrected": "Eu gosto de café",
                "explanation": "First-person present of gostar is 'gosto', not 'gosta'.",
            },
            {
                "type": "wording",
                "original": "Eu fico muito feliz",
                "corrected": "Fico super feliz",
                "explanation": "This phrasing sounds more natural in casual speech.",
            },
        ],
        "vocabulary_suggestions": [
            {"portuguese": "de vez em quando", "english": "once in a while", "reason": "Useful for describing frequency."},
        ],
    }
)


class FakeProvider(AIProvider):
    def __init__(self, reply: str):
        self.reply = reply
        self.received_messages: list[ChatMessage] | None = None
        self.received_json_mode: bool | None = None

    def generate_reply(self, messages: list[ChatMessage], json_mode: bool = False) -> str:
        self.received_messages = messages
        self.received_json_mode = json_mode
        return self.reply


@pytest.fixture()
def submission_repo(db_session, test_user):
    return WritingSubmissionRepository(db_session, test_user.id)


def test_review_persists_and_returns_submission(submission_repo):
    fake = FakeProvider(VALID_RESPONSE)
    service = WritingCoachService(submission_repo, provider_factory=lambda: fake)

    submission = service.review("Eu gosta de café.")

    assert submission.id is not None
    assert submission.original_text == "Eu gosta de café."
    assert submission.overall_feedback.startswith("Nice work")
    assert len(submission.corrections) == 2
    assert submission.corrections[0]["type"] == "grammar"
    assert submission.corrections[1]["type"] == "wording"
    assert len(submission.vocabulary_suggestions) == 1
    assert submission.vocabulary_suggestions[0]["portuguese"] == "de vez em quando"


def test_review_requests_json_mode(submission_repo):
    fake = FakeProvider(VALID_RESPONSE)
    service = WritingCoachService(submission_repo, provider_factory=lambda: fake)

    service.review("Some text")

    assert fake.received_json_mode is True


def test_review_sends_system_prompt_and_text_as_user_message(submission_repo):
    fake = FakeProvider(VALID_RESPONSE)
    service = WritingCoachService(submission_repo, provider_factory=lambda: fake)

    service.review("Eu gosta de café.")

    assert fake.received_messages[0].role == "system"
    assert fake.received_messages[1] == ChatMessage(role="user", content="Eu gosta de café.")


def test_malformed_json_raises_parse_error(submission_repo):
    fake = FakeProvider("this is not json at all")
    service = WritingCoachService(submission_repo, provider_factory=lambda: fake)

    with pytest.raises(AIResponseParseError):
        service.review("Some text")


def test_missing_required_fields_in_correction_are_dropped_not_crashed(submission_repo):
    response = json.dumps(
        {
            "overall_feedback": "Feedback here.",
            "corrections": [
                {"type": "grammar", "original": "x"},  # missing corrected/explanation
                {
                    "type": "grammar",
                    "original": "a",
                    "corrected": "b",
                    "explanation": "why",
                },
            ],
            "vocabulary_suggestions": [],
        }
    )
    fake = FakeProvider(response)
    service = WritingCoachService(submission_repo, provider_factory=lambda: fake)

    submission = service.review("Some text")

    assert len(submission.corrections) == 1  # the broken one got dropped
    assert submission.corrections[0]["original"] == "a"


def test_invalid_correction_type_defaults_to_grammar(submission_repo):
    response = json.dumps(
        {
            "overall_feedback": "Feedback.",
            "corrections": [
                {"type": "not-a-real-type", "original": "a", "corrected": "b", "explanation": "c"}
            ],
            "vocabulary_suggestions": [],
        }
    )
    fake = FakeProvider(response)
    service = WritingCoachService(submission_repo, provider_factory=lambda: fake)

    submission = service.review("text")

    assert submission.corrections[0]["type"] == "grammar"


def test_non_list_corrections_field_coerces_to_empty_list(submission_repo):
    response = json.dumps(
        {"overall_feedback": "Feedback.", "corrections": "not a list", "vocabulary_suggestions": None}
    )
    fake = FakeProvider(response)
    service = WritingCoachService(submission_repo, provider_factory=lambda: fake)

    submission = service.review("text")

    assert submission.corrections == []
    assert submission.vocabulary_suggestions == []


def test_review_raises_ai_feature_disabled_when_not_configured(submission_repo):
    def unconfigured_factory():
        raise AIFeatureDisabledError("no key set")

    service = WritingCoachService(submission_repo, provider_factory=unconfigured_factory)

    with pytest.raises(AIFeatureDisabledError):
        service.review("Some text")


def test_list_history_returns_most_recent_first(submission_repo):
    fake = FakeProvider(VALID_RESPONSE)
    service = WritingCoachService(submission_repo, provider_factory=lambda: fake)

    first = service.review("First submission")
    second = service.review("Second submission")

    history = service.list_history()
    assert history[0].id == second.id
    assert history[1].id == first.id


def test_get_or_404_returns_none_for_missing(submission_repo):
    service = WritingCoachService(submission_repo)
    assert service.get_or_404(999) is None
