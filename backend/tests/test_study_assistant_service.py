import pytest

from app.models.study_assistant import MessageRole
from app.repositories.study_assistant_repository import StudyAssistantRepository
from app.repositories.vocabulary_repository import VocabularyRepository
from app.services.ai.base import AIProvider, ChatMessage
from app.services.study_assistant_service import StudyAssistantService
from app.models.vocabulary import Vocabulary


def _make_vocab(db_session, user_id, portuguese, english, mastery_level=0):
    v = Vocabulary(portuguese=portuguese, english=english, user_id=user_id, mastery_level=mastery_level)
    v.tags = []
    db_session.add(v)
    db_session.commit()
    return v


class FakeProvider(AIProvider):
    def __init__(self, reply="Sure, let's practice!"):
        self.reply = reply
        self.last_messages = None

    def generate_reply(self, messages: list[ChatMessage], json_mode: bool = False) -> str:
        self.last_messages = messages
        return self.reply


@pytest.fixture()
def service(db_session, test_user):
    return StudyAssistantService(
        StudyAssistantRepository(db_session, test_user.id),
        VocabularyRepository(db_session, test_user.id),
    )


def test_context_summary_for_new_user_with_no_vocab(service):
    summary = service._build_context_summary()
    assert "hasn't added any vocabulary" in summary


def test_context_summary_includes_mastery_distribution_and_weak_words(db_session, test_user, service):
    _make_vocab(db_session, test_user.id, "falar", "to speak", mastery_level=0)
    _make_vocab(db_session, test_user.id, "comer", "to eat", mastery_level=1)
    _make_vocab(db_session, test_user.id, "andar", "to walk", mastery_level=4)

    summary = service._build_context_summary()

    assert "3 vocabulary word" in summary
    assert "falar (to speak)" in summary
    assert "comer (to eat)" in summary
    if "struggling with most" in summary:
        assert "andar" not in summary.split("struggling with most")[-1]


def test_ask_injects_context_and_history_into_the_system_prompt(db_session, test_user, service):
    _make_vocab(db_session, test_user.id, "falar", "to speak", mastery_level=0)
    fake = FakeProvider(reply="Let's try 'falar' — how would you say 'I speak'?")
    service.provider_factory = lambda: fake

    reply = service.ask("Can you help me practice?")

    assert reply == "Let's try 'falar' — how would you say 'I speak'?"
    assert fake.last_messages[0].role == "system"
    assert "falar" in fake.last_messages[0].content
    assert fake.last_messages[-1].content == "Can you help me practice?"


def test_ask_persists_both_sides_of_the_conversation(db_session, test_user, service):
    fake = FakeProvider(reply="Great question!")
    service.provider_factory = lambda: fake

    service.ask("Why is 'ser' different from 'estar'?")

    history = service.get_history()
    assert len(history) == 2
    assert history[0].role == MessageRole.user
    assert history[0].content == "Why is 'ser' different from 'estar'?"
    assert history[1].role == MessageRole.assistant
    assert history[1].content == "Great question!"


def test_ask_includes_prior_turns_in_the_next_call(db_session, test_user, service):
    fake = FakeProvider(reply="First reply")
    service.provider_factory = lambda: fake
    service.ask("First question")

    fake2 = FakeProvider(reply="Second reply")
    service.provider_factory = lambda: fake2
    service.ask("Second question")

    contents = [m.content for m in fake2.last_messages]
    assert "First question" in contents
    assert "First reply" in contents
    assert "Second question" in contents


def test_clear_history_removes_all_messages(db_session, test_user, service):
    fake = FakeProvider()
    service.provider_factory = lambda: fake
    service.ask("A question")
    assert len(service.get_history()) == 2

    service.clear_history()

    assert service.get_history() == []


def test_failed_ai_call_does_not_persist_a_one_sided_message(db_session, test_user, service):
    class FailingProvider(AIProvider):
        def generate_reply(self, messages, json_mode=False):
            raise RuntimeError("simulated failure")

    service.provider_factory = lambda: FailingProvider()

    with pytest.raises(RuntimeError):
        service.ask("This will fail")

    assert service.get_history() == []
