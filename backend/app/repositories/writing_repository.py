from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.writing import WritingSubmission


class WritingSubmissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, submission: WritingSubmission) -> WritingSubmission:
        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)
        return submission

    def list(self, limit: int = 20) -> list[WritingSubmission]:
        stmt = (
            select(WritingSubmission)
            .order_by(WritingSubmission.created_at.desc())
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())

    def get(self, submission_id: int) -> WritingSubmission | None:
        return self.db.get(WritingSubmission, submission_id)
