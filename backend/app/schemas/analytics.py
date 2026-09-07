from pydantic import BaseModel


class VocabularyGrowthPoint(BaseModel):
    date: str
    count: int
    cumulative: int


class ReviewActivityPoint(BaseModel):
    date: str
    count: int


class ReviewQualityPoint(BaseModel):
    date: str
    again: int
    hard: int
    medium: int
    easy: int


class MasteryTrendPoint(BaseModel):
    date: str
    level_0: int
    level_1: int
    level_2: int
    level_3: int
    level_4: int
    level_5: int


class WritingInsightPoint(BaseModel):
    date: str
    grammar: int
    wording: int


class AnalyticsSummary(BaseModel):
    vocabulary_growth: list[VocabularyGrowthPoint]
    review_activity: list[ReviewActivityPoint]
    review_quality: list[ReviewQualityPoint]
    mastery_trend: list[MasteryTrendPoint]
    writing_insights: list[WritingInsightPoint]


class DashboardWidgetsUpdate(BaseModel):
    widgets: list[str]
