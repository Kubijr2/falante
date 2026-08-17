from typing import Literal

from pydantic import BaseModel, Field


class TutorMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class TutorRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    topic_slug: str | None = None
    # Prior turns in this conversation, oldest first. Not persisted anywhere
    # server-side — the frontend owns the running transcript and resends it
    # each time, which is what "multi-turn, no backend session state" means.
    history: list[TutorMessage] = Field(default_factory=list)


class TutorResponse(BaseModel):
    answer: str


class TutorStatus(BaseModel):
    enabled: bool
