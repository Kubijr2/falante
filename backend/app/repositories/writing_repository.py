from __future__ import annotations

from datetime import date

from sqlalchemy import func, select
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

    def list_dates_and_corrections(self, start_date: date | None) -> list[tuple[date, str | None]]:
        """
        Every submission's date + raw corrections JSON — used to tally
        grammar-vs-wording correction counts per day for the writing
        insights chart. Returned raw (not parsed) since parsing the JSON is
        the service layer's job, not the repository's.
        """
        stmt = select(
            func.date(WritingSubmission.created_at), WritingSubmission.corrections_raw
        ).where(WritingSubmission.user_id == self.user_id)
        if start_date is not None:
            stmt = stmt.where(WritingSubmission.created_at >= start_date)
        rows = self.db.execute(stmt).all()
        return [
            (d if isinstance(d, date) else date.fromisoformat(d), corrections_raw)
            for d, corrections_raw in rows
        ]
