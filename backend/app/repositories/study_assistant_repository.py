from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.study_assistant import MessageRole, StudyAssistantMessage


class StudyAssistantRepository:
    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id

    def list_messages(self) -> list[StudyAssistantMessage]:
        stmt = (
            select(StudyAssistantMessage)
            .where(StudyAssistantMessage.user_id == self.user_id)
            .order_by(StudyAssistantMessage.created_at.asc())
        )
        return list(self.db.execute(stmt).scalars().all())

    def add_message(self, role: MessageRole, content: str) -> StudyAssistantMessage:
        message = StudyAssistantMessage(user_id=self.user_id, role=role, content=content)
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def clear(self) -> None:
        stmt = delete(StudyAssistantMessage).where(StudyAssistantMessage.user_id == self.user_id)
        self.db.execute(stmt)
        self.db.commit()
