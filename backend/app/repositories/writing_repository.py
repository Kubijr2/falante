from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.writing import WritingSubmission


class WritingSubmissionRepository:
    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id

    def create(self, submission: WritingSubmission) -> WritingSubmission:
        submission.user_id = self.user_id
        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)
        return submission

    def list(self, limit: int = 20) -> list[WritingSubmission]:
        stmt = (
            select(WritingSubmission)
            .where(WritingSubmission.user_id == self.user_id)
            .order_by(WritingSubmission.created_at.desc())
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())

    def get(self, submission_id: int) -> WritingSubmission | None:
        stmt = select(WritingSubmission).where(
            WritingSubmission.id == submission_id, WritingSubmission.user_id == self.user_id
        )
        return self.db.execute(stmt).scalar_one_or_none()
