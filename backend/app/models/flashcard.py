import enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ReviewResult(str, enum.Enum):
    again = "again"
    hard = "hard"
    medium = "medium"
    easy = "easy"


class FlashcardReview(Base):
    """
    One row per review event. This table is intentionally append-only —
    it becomes the data source for Progress Analytics later (Milestone 8)
    without needing a new table.
    """

    __tablename__ = "flashcard_reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vocabulary_id: Mapped[int] = mapped_column(ForeignKey("vocabulary.id"), nullable=False)
    reviewed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    result: Mapped[ReviewResult] = mapped_column(Enum(ReviewResult), nullable=False)
    interval_days_before: Mapped[int] = mapped_column(Integer, nullable=False)
    interval_days_after: Mapped[int] = mapped_column(Integer, nullable=False)

    vocabulary = relationship("Vocabulary", back_populates="reviews")
