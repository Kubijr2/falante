import json
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class WritingSubmission(Base):
    """
    One row per piece of writing the learner submits to the AI Writing
    Coach. `corrections` and `vocabulary_suggestions` are stored as JSON —
    same pattern as Vocabulary.tags and Verb.irregular_conjugations
    elsewhere in this codebase — since they're generated content specific
    to this one submission, not data anything else needs to query into.
    """

    __tablename__ = "writing_submissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    original_text: Mapped[str] = mapped_column(Text, nullable=False)
    overall_feedback: Mapped[str] = mapped_column(Text, nullable=False, default="")
    corrections_raw: Mapped[str | None] = mapped_column("corrections", Text, nullable=True)
    vocabulary_suggestions_raw: Mapped[str | None] = mapped_column(
        "vocabulary_suggestions", Text, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    @property
    def corrections(self) -> list[dict]:
        return json.loads(self.corrections_raw) if self.corrections_raw else []

    @corrections.setter
    def corrections(self, value: list[dict]) -> None:
        self.corrections_raw = json.dumps(value) if value else None

    @property
    def vocabulary_suggestions(self) -> list[dict]:
        return json.loads(self.vocabulary_suggestions_raw) if self.vocabulary_suggestions_raw else []

    @vocabulary_suggestions.setter
    def vocabulary_suggestions(self, value: list[dict]) -> None:
        self.vocabulary_suggestions_raw = json.dumps(value) if value else None
