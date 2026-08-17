from datetime import datetime

from pydantic import BaseModel, ConfigDict


class GrammarTopicListItem(BaseModel):
    """Used by the list endpoint — no `content`, so browsing stays lightweight."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    category: str
    summary: str


class GrammarTopicDetail(GrammarTopicListItem):
    """Used by the single-topic endpoint — includes the full Markdown body."""

    content: str
    created_at: datetime
    updated_at: datetime
