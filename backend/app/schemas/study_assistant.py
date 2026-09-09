from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StudyAssistantMessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    content: str
    created_at: datetime


class StudyAssistantAskRequest(BaseModel):
    message: str


class StudyAssistantAskResponse(BaseModel):
    reply: str
