from __future__ import annotations

from app.models.study_assistant import MessageRole
from app.repositories.study_assistant_repository import StudyAssistantRepository
from app.repositories.vocabulary_repository import VocabularyRepository
from app.services.ai.base import ChatMessage
from app.services.ai.factory import get_ai_provider

SYSTEM_PROMPT_TEMPLATE = """You are Falante's AI Study Assistant — a friendly, encouraging \
Brazilian Portuguese study companion, available to the student on every page of the app.

Your job is to help the student practice and think for themselves, not to just hand them \
answers. Prefer guiding questions and hints over direct answers; encourage them to attempt \
something themselves before you confirm or correct it. Keep replies conversational and \
reasonably short — this is a chat, not an essay.

Here is what you currently know about this student's real progress in the app:
{context_summary}

Use this naturally when it's relevant — for example, suggesting they practice a specific word \
they're struggling with — but don't force it into every reply, and don't repeat the same \
suggestion over and over if they don't take it up.
"""


class StudyAssistantService:
    def __init__(
        self,
        message_repo: StudyAssistantRepository,
        vocabulary_repo: VocabularyRepository,
        provider_factory=get_ai_provider,
    ):
        self.message_repo = message_repo
        self.vocabulary_repo = vocabulary_repo
        self.provider_factory = provider_factory

    def get_history(self):
        return self.message_repo.list_messages()

    def clear_history(self) -> None:
        self.message_repo.clear()

    def ask(self, user_message: str) -> str:
        provider = self.provider_factory()

        history = self.message_repo.list_messages()
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            context_summary=self._build_context_summary()
        )

        messages = [ChatMessage(role="system", content=system_prompt)]
        messages += [ChatMessage(role=m.role.value, content=m.content) for m in history]
        messages.append(ChatMessage(role="user", content=user_message))

        reply = provider.generate_reply(messages)

        # Persist both sides — done after a successful AI call so a failed
        # call doesn't leave a one-sided message in the saved history.
        self.message_repo.add_message(MessageRole.user, user_message)
        self.message_repo.add_message(MessageRole.assistant, reply)

        return reply

    def _build_context_summary(self) -> str:
        total = self.vocabulary_repo.count_total()
        if total == 0:
            return "This student hasn't added any vocabulary yet — they're just getting started."

        distribution = self.vocabulary_repo.mastery_distribution()
        distribution_desc = ", ".join(
            f"level {level}: {count}" for level, count in sorted(distribution.items())
        )

        weakest = self.vocabulary_repo.lowest_mastery_words(limit=8)
        struggling = [w for w in weakest if w.mastery_level <= 1]
        lines = [
            f"They have {total} vocabulary word(s) saved.",
            f"Mastery levels (0 = brand new, 5 = mastered): {distribution_desc}.",
        ]
        if struggling:
            words_desc = ", ".join(f"{w.portuguese} ({w.english})" for w in struggling)
            lines.append(f"Words they're currently struggling with most: {words_desc}.")

        return " ".join(lines)
