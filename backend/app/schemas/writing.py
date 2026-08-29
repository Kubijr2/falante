from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Correction(BaseModel):
    type: Literal["grammar", "wording"]
    original: str
    corrected: str
    explanation: str


class VocabularySuggestion(BaseModel):
    portuguese: str
    english: str
    reason: str


class WritingSubmissionCreate(BaseModel):
    text: str = Field(min_length=1, max_length=4000)


class WritingSubmissionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    original_text: str
    overall_feedback: str
    corrections: list[Correction]
    vocabulary_suggestions: list[VocabularySuggestion]
    created_at: datetime
