from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Verb(Base):
    __tablename__ = "verbs"

    id: Mapped[int] = mapped_column(primary_key=True)
    infinitive: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    translation: Mapped[str] = mapped_column(String(200), nullable=False)
    is_irregular: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # Only set for irregular verbs — a JSON-encoded {tense: [4 forms]} blob
    # that overrides the conjugation engine entirely for that verb. NULL for
    # every regular verb, whose forms are always computed on the fly by
    # conjugation_engine.conjugate_regular() instead of being stored.
    irregular_conjugations: Mapped[str | None] = mapped_column(Text, nullable=True)
