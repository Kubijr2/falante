import enum
import json
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
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
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    portuguese: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    english: Mapped[str] = mapped_column(String(200), nullable=False)
    example_sentence: Mapped[str | None] = mapped_column(String(500), nullable=True)
    notes: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    tags_raw: Mapped[str | None] = mapped_column("tags", String(500), nullable=True)
    difficulty: Mapped[Difficulty] = mapped_column(
        Enum(Difficulty), default=Difficulty.medium, nullable=False
    )
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
