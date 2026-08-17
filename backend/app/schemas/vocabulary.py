from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.vocabulary import Difficulty


class VocabularyBase(BaseModel):
    portuguese: str = Field(min_length=1, max_length=200)
    english: str = Field(min_length=1, max_length=200)
    example_sentence: str | None = Field(default=None, max_length=500)
    notes: str | None = Field(default=None, max_length=1000)
    category: str | None = Field(default=None, max_length=100)
    tags: list[str] = Field(default_factory=list)
    difficulty: Difficulty = Difficulty.medium


class VocabularyCreate(VocabularyBase):
    pass


class VocabularyUpdate(BaseModel):
    """All fields optional — PATCH semantics."""

    portuguese: str | None = Field(default=None, min_length=1, max_length=200)
    english: str | None = Field(default=None, min_length=1, max_length=200)
    example_sentence: str | None = None
    notes: str | None = None
    category: str | None = None
    tags: list[str] | None = None
    difficulty: Difficulty | None = None


class VocabularyRead(VocabularyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    mastery_level: int
    next_review_at: datetime
    created_at: datetime
    updated_at: datetime
