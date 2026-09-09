from __future__ import annotations

from datetime import date

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

    def lowest_mastery_words(self, limit: int) -> list[Vocabulary]:
        stmt = (
            select(Vocabulary)
            .where(Vocabulary.user_id == self.user_id)
            .order_by(Vocabulary.mastery_level.asc(), Vocabulary.created_at.desc())
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())

    def count_by_day(self, start_date: date | None) -> list[tuple[str, int]]:
        """Rows added per day — the raw material for the vocabulary growth chart."""
        stmt = select(func.date(Vocabulary.created_at), func.count()).where(
            Vocabulary.user_id == self.user_id
        )
        if start_date is not None:
            stmt = stmt.where(Vocabulary.created_at >= start_date)
        stmt = stmt.group_by(func.date(Vocabulary.created_at)).order_by(
            func.date(Vocabulary.created_at)
        )
        return list(self.db.execute(stmt).all())

    def count_before(self, start_date: date) -> int:
        """
        How many words existed before the visible range starts — needed so
        a filtered chart (e.g. "last 30 days") shows a correct running
        total instead of restarting from zero at the window's edge.
        """
        stmt = (
            select(func.count())
            .select_from(Vocabulary)
            .where(Vocabulary.user_id == self.user_id, Vocabulary.created_at < start_date)
        )
        return self.db.execute(stmt).scalar_one()

    def list_id_and_created_date(self) -> list[tuple[int, date]]:
        """
        Every word's id + creation date, full history regardless of any
        display range — used to replay mastery level changes chronologically
        for the mastery trend chart, which needs the complete history to
        compute an accurate starting point for any requested window.
        """
        stmt = select(Vocabulary.id, func.date(Vocabulary.created_at)).where(
            Vocabulary.user_id == self.user_id
        )
        rows = self.db.execute(stmt).all()
        return [(vid, d if isinstance(d, date) else date.fromisoformat(d)) for vid, d in rows]
