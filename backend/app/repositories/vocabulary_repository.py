from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.vocabulary import Vocabulary


class VocabularyRepository:
    """
    Owns every direct SQLAlchemy query for the Vocabulary table.
    Services depend on this instead of touching `db.query(...)` themselves —
    if we ever change ORMs or add caching, only this file changes.
    """

    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        category: str | None = None,
        search: str | None = None,
    ) -> list[Vocabulary]:
        stmt = select(Vocabulary)
        if category:
            stmt = stmt.where(Vocabulary.category == category)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(
                (Vocabulary.portuguese.ilike(like)) | (Vocabulary.english.ilike(like))
            )
        stmt = stmt.order_by(Vocabulary.created_at.desc())
        return list(self.db.execute(stmt).scalars().all())

    def get(self, vocabulary_id: int) -> Vocabulary | None:
        return self.db.get(Vocabulary, vocabulary_id)

    def create(self, vocabulary: Vocabulary) -> Vocabulary:
        self.db.add(vocabulary)
        self.db.commit()
        self.db.refresh(vocabulary)
        return vocabulary

    def update(self, vocabulary: Vocabulary) -> Vocabulary:
        self.db.commit()
        self.db.refresh(vocabulary)
        return vocabulary

    def delete(self, vocabulary: Vocabulary) -> None:
        self.db.delete(vocabulary)
        self.db.commit()

    def due_for_review(self, now) -> list[Vocabulary]:
        stmt = select(Vocabulary).where(Vocabulary.next_review_at <= now)
        return list(self.db.execute(stmt).scalars().all())

    def count_total(self) -> int:
        stmt = select(func.count()).select_from(Vocabulary)
        return self.db.execute(stmt).scalar_one()

    def mastery_distribution(self) -> dict[int, int]:
        """Count of words at each mastery level, 0-5, always including empty levels."""
        stmt = select(Vocabulary.mastery_level, func.count()).group_by(Vocabulary.mastery_level)
        counts = dict(self.db.execute(stmt).all())
        return {level: counts.get(level, 0) for level in range(6)}
