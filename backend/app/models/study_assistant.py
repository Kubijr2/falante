import enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class MessageRole(str, enum.Enum):
    user = "user"
    assistant = "assistant"


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class StudyAssistantMessage(Base):
    """
    One row per message in the Study Assistant's persistent chat — a
    single, ever-growing thread per user (not multiple named sessions).
    This matches the floating-chat-bubble UX: open it from any page, see
    the same ongoing conversation, keep going. "Clear conversation"
    deletes all of a user's rows to start fresh, rather than the app
    managing a list of separate sessions.
    """

    __tablename__ = "study_assistant_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    role: Mapped[MessageRole] = mapped_column(Enum(MessageRole, name="studyassistantrole"))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
