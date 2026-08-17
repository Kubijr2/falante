from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.verb import Verb


class VerbRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, search: str | None = None) -> list[Verb]:
        stmt = select(Verb)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(
                (Verb.infinitive.ilike(like)) | (Verb.translation.ilike(like))
            )
        stmt = stmt.order_by(Verb.infinitive)
        return list(self.db.execute(stmt).scalars().all())

    def get_by_infinitive(self, infinitive: str) -> Verb | None:
        stmt = select(Verb).where(Verb.infinitive == infinitive)
        return self.db.execute(stmt).scalar_one_or_none()
