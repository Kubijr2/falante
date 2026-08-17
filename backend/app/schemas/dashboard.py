from pydantic import BaseModel

from app.schemas.vocabulary import VocabularyRead


class DashboardSummary(BaseModel):
    streak: int
    total_words: int
    due_today: int
    total_reviews: int
    mastery_distribution: dict[int, int]
    recently_learned: list[VocabularyRead]
