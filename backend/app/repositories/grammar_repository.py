from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.grammar import GrammarTopic


class GrammarRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, category: str | None = None, search: str | None = None) -> list[GrammarTopic]:
        stmt = select(GrammarTopic)
        if category:
            stmt = stmt.where(GrammarTopic.category == category)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(
                (GrammarTopic.title.ilike(like))
                | (GrammarTopic.summary.ilike(like))
                | (GrammarTopic.content.ilike(like))
            )
        stmt = stmt.order_by(GrammarTopic.category, GrammarTopic.title)
        return list(self.db.execute(stmt).scalars().all())

    def get_by_slug(self, slug: str) -> GrammarTopic | None:
        stmt = select(GrammarTopic).where(GrammarTopic.slug == slug)
        return self.db.execute(stmt).scalar_one_or_none()

    def list_categories(self) -> list[str]:
        stmt = select(GrammarTopic.category).distinct().order_by(GrammarTopic.category)
        return list(self.db.execute(stmt).scalars().all())
