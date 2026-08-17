from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.flashcard import ReviewResult
from app.schemas.vocabulary import VocabularyRead


class ReviewSubmit(BaseModel):
    result: ReviewResult


class ReviewRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vocabulary_id: int
    reviewed_at: datetime
    result: ReviewResult
    interval_days_before: int
    interval_days_after: int


class DueCard(BaseModel):
    """What the frontend actually needs to render a due flashcard."""

    vocabulary: VocabularyRead
