from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.vocabulary import Vocabulary


class VocabularyRepository:
    """
    Scoped to one user for the lifetime of the request — every query is
    automatically filtered to `user_id`, and `create()` stamps it on new
    rows. This is what makes it structurally impossible for a route to
    "forget" the user filter on any one query: it isn't a parameter you
    might omit, it's baked into the repository instance itself.
    """

    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id

    def list(self, category: str | None = None, search: str | None = None) -> list[Vocabulary]:
        stmt = select(Vocabulary).where(Vocabulary.user_id == self.user_id)
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
        # Filtering by user_id here (not just id) means a mismatched id
        # simply looks like "not found" rather than leaking whether that id
        # belongs to someone else.
        stmt = select(Vocabulary).where(
            Vocabulary.id == vocabulary_id, Vocabulary.user_id == self.user_id
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def create(self, vocabulary: Vocabulary) -> Vocabulary:
        vocabulary.user_id = self.user_id
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
        stmt = select(Vocabulary).where(
            Vocabulary.user_id == self.user_id, Vocabulary.next_review_at <= now
        )
        return list(self.db.execute(stmt).scalars().all())

    def count_total(self) -> int:
        stmt = (
            select(func.count())
            .select_from(Vocabulary)
            .where(Vocabulary.user_id == self.user_id)
        )
        return self.db.execute(stmt).scalar_one()

    def mastery_distribution(self) -> dict[int, int]:
        stmt = (
            select(Vocabulary.mastery_level, func.count())
            .where(Vocabulary.user_id == self.user_id)
            .group_by(Vocabulary.mastery_level)
        )
        counts = dict(self.db.execute(stmt).all())
        return {level: counts.get(level, 0) for level in range(6)}
