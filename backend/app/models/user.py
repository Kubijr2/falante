import json
from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    # Google's stable unique identifier for the account ("sub" claim in the
    # ID token) — used to look up the same user on every subsequent login,
    # since email addresses can technically change on Google's side.
    google_sub: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    picture_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    # Which analytics widgets this account has chosen to pin to their
    # Dashboard (Milestone 11) — e.g. ["vocabulary_growth", "review_activity"].
    # JSON-encoded, same pattern as Vocabulary.tags — this is a per-account
    # UI preference, not something anything else needs to query into.
    dashboard_widgets_raw: Mapped[str | None] = mapped_column(
        "dashboard_widgets", Text, nullable=True
    )

    @property
    def dashboard_widgets(self) -> list[str]:
        return json.loads(self.dashboard_widgets_raw) if self.dashboard_widgets_raw else []

    @dashboard_widgets.setter
    def dashboard_widgets(self, value: list[str]) -> None:
        self.dashboard_widgets_raw = json.dumps(value) if value else None
