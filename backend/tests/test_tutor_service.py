import pytest

from app.repositories.grammar_repository import GrammarRepository
from app.services.ai.base import AIProvider, ChatMessage
from app.services.ai.factory import AIFeatureDisabledError
from app.services.tutor_service import TutorService


class FakeProvider(AIProvider):
    """Records what it was called with instead of hitting a real API."""

    def __init__(self, reply: str = "Here's the explanation."):
        self.reply = reply
        self.received_messages: list[ChatMessage] | None = None

    def generate_reply(self, messages: list[ChatMessage]) -> str:
        self.received_messages = messages
        return self.reply


@pytest.fixture()
def grammar_repo(db_session):
    # db_session (from conftest.py) already seeds GRAMMAR_TOPICS — no need
    # to add them again here.
    return GrammarRepository(db_session)


def test_ask_returns_provider_reply(grammar_repo):
    fake = FakeProvider(reply="Ser is for permanent traits.")
    service = TutorService(grammar_repo, provider_factory=lambda: fake)

    answer = service.ask("Why ser here?", history=[], topic_slug=None)

    assert answer == "Ser is for permanent traits."


def test_ask_includes_system_prompt_first(grammar_repo):
    fake = FakeProvider()
    service = TutorService(grammar_repo, provider_factory=lambda: fake)

    service.ask("A question", history=[], topic_slug=None)

    assert fake.received_messages[0].role == "system"
    assert "teach" in fake.received_messages[0].content.lower()


def test_ask_includes_topic_content_as_context_when_slug_given(grammar_repo):
    fake = FakeProvider()
    service = TutorService(grammar_repo, provider_factory=lambda: fake)

    service.ask("Why?", history=[], topic_slug="ser-vs-estar")

    system_message = fake.received_messages[0]
    assert "Ser vs. Estar" in system_message.content
    assert "The core distinction" in system_message.content  # from the article body


def test_ask_without_topic_slug_has_no_article_context(grammar_repo):
    fake = FakeProvider()
    service = TutorService(grammar_repo, provider_factory=lambda: fake)

    service.ask("General question", history=[], topic_slug=None)

    assert "currently reading" not in fake.received_messages[0].content


def test_ask_unknown_slug_does_not_crash(grammar_repo):
    fake = FakeProvider()
    service = TutorService(grammar_repo, provider_factory=lambda: fake)

    # Should silently skip adding context rather than error, since a bad
    # slug shouldn't take down the whole tutor feature.
    answer = service.ask("Question", history=[], topic_slug="not-a-real-slug")
    assert answer == fake.reply


def test_ask_passes_conversation_history_in_order(grammar_repo):
    fake = FakeProvider()
    service = TutorService(grammar_repo, provider_factory=lambda: fake)

    history = [
        ChatMessage(role="user", content="First question"),
        ChatMessage(role="assistant", content="First answer"),
    ]
    service.ask("Follow-up question", history=history, topic_slug=None)

    roles_and_content = [(m.role, m.content) for m in fake.received_messages]
    assert roles_and_content == [
        ("system", fake.received_messages[0].content),
        ("user", "First question"),
        ("assistant", "First answer"),
        ("user", "Follow-up question"),
    ]


def test_ask_raises_ai_feature_disabled_when_no_provider_configured(grammar_repo):
    def unconfigured_factory():
        raise AIFeatureDisabledError("no key set")

    service = TutorService(grammar_repo, provider_factory=unconfigured_factory)

    with pytest.raises(AIFeatureDisabledError):
        service.ask("A question", history=[], topic_slug=None)
