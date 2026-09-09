from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.current_user import get_current_user
from app.core.database import get_db
from app.core.rate_limit import limiter
from app.models.user import User
from app.repositories.study_assistant_repository import StudyAssistantRepository
from app.repositories.vocabulary_repository import VocabularyRepository
from app.schemas.study_assistant import (
    StudyAssistantAskRequest,
    StudyAssistantAskResponse,
    StudyAssistantMessageRead,
)
from app.services.ai.factory import AIFeatureDisabledError
from app.services.study_assistant_service import StudyAssistantService

router = APIRouter(prefix="/study-assistant", tags=["study-assistant"])


def get_service(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> StudyAssistantService:
    return StudyAssistantService(
        StudyAssistantRepository(db, current_user.id),
        VocabularyRepository(db, current_user.id),
    )


@router.get("", response_model=list[StudyAssistantMessageRead])
def get_history(service: StudyAssistantService = Depends(get_service)):
    return service.get_history()


@router.post("/message", response_model=StudyAssistantAskResponse)
@limiter.limit(lambda: f"{settings.ai_rate_limit_per_day}/day")
def send_message(
    request: Request,  # required by slowapi to identify the caller — unused otherwise
    payload: StudyAssistantAskRequest,
    service: StudyAssistantService = Depends(get_service),
):
    try:
        reply = service.ask(payload.message)
    except AIFeatureDisabledError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
    return StudyAssistantAskResponse(reply=reply)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def clear_history(service: StudyAssistantService = Depends(get_service)):
    service.clear_history()
