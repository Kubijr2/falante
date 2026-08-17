from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class GrammarTopic(Base):
    __tablename__ = "grammar_topics"

    id: Mapped[int] = mapped_column(primary_key=True)
    # URL-friendly identifier, e.g. "ser-vs-estar" — used for detail routes
    # instead of exposing raw DB ids in the URL.
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    # One-line teaser shown in the list view, kept separate from `content` so
    # the list endpoint can stay lightweight (see schemas/grammar.py).
    summary: Mapped[str] = mapped_column(String(300), nullable=False)
    # Full article body, Markdown. Deliberately a plain Text column with no
    # further structure — this is also the field a future AI explanation
    # feature (Milestone 5) will read as context, and Markdown is a format
    # both humans and an LLM handle well.
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow
    )
