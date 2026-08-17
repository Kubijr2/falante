from __future__ import annotations

from collections.abc import Callable

from app.repositories.grammar_repository import GrammarRepository
from app.services.ai.base import ChatMessage
from app.services.ai.factory import get_ai_provider

SYSTEM_PROMPT = """You are a patient, encouraging Brazilian Portuguese grammar tutor inside a study app called Falante.

Your job is to teach, not just translate or give one-line answers. When a learner asks a question:
- Explain the underlying grammar rule or pattern, not just the specific answer.
- Use a short example sentence in Portuguese with an English gloss when it helps.
- Keep answers focused and concise — a few short paragraphs at most, not a full essay.
- If it's natural, end with a brief follow-up question or a related tip, but don't force one every time.
- If the learner seems to want a plain translation, still frame your answer around the grammar reasoning.
"""


class TutorService:
    def __init__(
        self,
        grammar_repo: GrammarRepository,
        provider_factory: Callable | None = None,
    ):
        self.grammar_repo = grammar_repo
        # Not a default *parameter* value on purpose — a default arg would
        # bind to get_ai_provider at class-definition time, which is awkward
        # to override in tests. Resolving it lazily in ask() means tests can
        # either pass their own provider_factory or monkeypatch the
        # module-level get_ai_provider and have it actually take effect.
        self._provider_factory = provider_factory

    def ask(
        self,
        question: str,
        history: list[ChatMessage],
        topic_slug: str | None,
    ) -> str:
        factory = self._provider_factory or get_ai_provider
        provider = factory()  # raises AIFeatureDisabledError if not configured

        system_content = SYSTEM_PROMPT
        if topic_slug:
            topic = self.grammar_repo.get_by_slug(topic_slug)
            if topic:
                system_content += (
                    f"\n\nThe learner is currently reading this grammar article, "
                    f"\"{topic.title}\":\n\n{topic.content}\n\n"
                    "You can reference it directly when it's relevant to their question."
                )

        messages = [ChatMessage(role="system", content=system_content)]
        messages.extend(history)
        messages.append(ChatMessage(role="user", content=question))

        return provider.generate_reply(messages)
