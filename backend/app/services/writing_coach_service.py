from __future__ import annotations

import json
from collections.abc import Callable

from app.models.writing import WritingSubmission
from app.repositories.writing_repository import WritingSubmissionRepository
from app.services.ai.base import ChatMessage
from app.services.ai.factory import get_ai_provider

SYSTEM_PROMPT = """You are a Brazilian Portuguese writing coach inside a study app called Falante.

The learner will paste a piece of their own Portuguese writing. Analyze it and respond with ONLY a valid JSON object — no markdown code fences, no commentary before or after it — matching exactly this shape:

{
  "overall_feedback": "<one short encouraging paragraph, 2-3 sentences>",
  "corrections": [
    {"type": "grammar" | "wording", "original": "<the exact phrase from their text>", "corrected": "<the fixed or improved version>", "explanation": "<why, teaching the underlying rule, 1-2 sentences>"}
  ],
  "vocabulary_suggestions": [
    {"portuguese": "<word or phrase>", "english": "<meaning>", "reason": "<why it's relevant to what they wrote, 1 sentence>"}
  ]
}

Rules:
- "grammar" corrections are outright errors (wrong verb form, wrong gender agreement, wrong preposition, etc).
- "wording" corrections are not errors but sound unnatural — suggest how a native speaker would phrase it instead.
- Only include real, specific corrections tied to their actual text — don't invent problems in writing that's already correct. An empty corrections list is a perfectly good result for clean writing.
- Vocabulary suggestions should be words or phrases that would help the learner express similar ideas more naturally or precisely next time — aim for 2 to 5 suggestions.
- If the input isn't Portuguese at all, or is empty/nonsensical, say so plainly in overall_feedback and return empty lists for the other two fields.
"""


class AIResponseParseError(Exception):
    """Raised when the AI's reply can't be parsed into the expected structure."""


class WritingCoachService:
    def __init__(
        self,
        submission_repo: WritingSubmissionRepository,
        provider_factory: Callable | None = None,
    ):
        self.submission_repo = submission_repo
        self._provider_factory = provider_factory

    def review(self, text: str) -> WritingSubmission:
        factory = self._provider_factory or get_ai_provider
        provider = factory()  # raises AIFeatureDisabledError if not configured

        messages = [
            ChatMessage(role="system", content=SYSTEM_PROMPT),
            ChatMessage(role="user", content=text),
        ]
        raw = provider.generate_reply(messages, json_mode=True)
        parsed = self._parse_response(raw)

        submission = WritingSubmission(
            original_text=text,
            overall_feedback=parsed["overall_feedback"],
        )
        submission.corrections = parsed["corrections"]
        submission.vocabulary_suggestions = parsed["vocabulary_suggestions"]
        return self.submission_repo.create(submission)

    def list_history(self, limit: int = 20) -> list[WritingSubmission]:
        return self.submission_repo.list(limit=limit)

    def get_or_404(self, submission_id: int) -> WritingSubmission | None:
        return self.submission_repo.get(submission_id)

    def _parse_response(self, raw: str) -> dict:
        """
        Defensive on purpose: even with json_mode on, a model can occasionally
        drift from the exact requested shape. Rather than let a malformed
        field take down the whole request, coerce what we reasonably can and
        only fail hard when the response is unusable.
        """
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise AIResponseParseError("The AI's response wasn't valid JSON.") from exc

        if not isinstance(data, dict):
            raise AIResponseParseError("The AI's response wasn't a JSON object.")

        overall_feedback = data.get("overall_feedback")
        if not isinstance(overall_feedback, str):
            overall_feedback = ""

        corrections = self._coerce_corrections(data.get("corrections"))
        vocabulary_suggestions = self._coerce_vocabulary(data.get("vocabulary_suggestions"))

        return {
            "overall_feedback": overall_feedback,
            "corrections": corrections,
            "vocabulary_suggestions": vocabulary_suggestions,
        }

    @staticmethod
    def _coerce_corrections(raw_corrections) -> list[dict]:
        if not isinstance(raw_corrections, list):
            return []
        result = []
        for item in raw_corrections:
            if not isinstance(item, dict):
                continue
            if not all(k in item for k in ("original", "corrected", "explanation")):
                continue
            correction_type = item.get("type")
            if correction_type not in ("grammar", "wording"):
                correction_type = "grammar"  # reasonable default rather than dropping the item
            result.append(
                {
                    "type": correction_type,
                    "original": str(item["original"]),
                    "corrected": str(item["corrected"]),
                    "explanation": str(item["explanation"]),
                }
            )
        return result

    @staticmethod
    def _coerce_vocabulary(raw_vocab) -> list[dict]:
        if not isinstance(raw_vocab, list):
            return []
        result = []
        for item in raw_vocab:
            if not isinstance(item, dict):
                continue
            if not all(k in item for k in ("portuguese", "english")):
                continue
            result.append(
                {
                    "portuguese": str(item["portuguese"]),
                    "english": str(item["english"]),
                    "reason": str(item.get("reason", "")),
                }
            )
        return result
