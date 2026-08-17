import enum
import json
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Difficulty(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Vocabulary(Base):
    __tablename__ = "vocabulary"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    portuguese: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    english: Mapped[str] = mapped_column(String(200), nullable=False)
    example_sentence: Mapped[str | None] = mapped_column(String(500), nullable=True)
    notes: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    # Stored as a JSON-encoded list of strings, e.g. '["verbs", "food"]'.
    # SQLite has no native array type; this keeps the column portable to
    # Postgres too (where it could later become a real ARRAY or JSONB column).
    # The `tags` property below exposes/accepts a plain list[str] so nothing
    # outside this file needs to know about the JSON encoding.
    tags_raw: Mapped[str | None] = mapped_column("tags", String(500), nullable=True)
    difficulty: Mapped[Difficulty] = mapped_column(
        Enum(Difficulty), default=Difficulty.medium, nullable=False
    )
    # 0-5, drives spaced-repetition interval. See app/services/srs_service.py.
    mastery_level: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    next_review_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow
    )

    reviews = relationship(
        "FlashcardReview", back_populates="vocabulary", cascade="all, delete-orphan"
    )

    @property
    def tags(self) -> list[str]:
        return json.loads(self.tags_raw) if self.tags_raw else []

    @tags.setter
    def tags(self, value: list[str]) -> None:
        self.tags_raw = json.dumps(value) if value else None
