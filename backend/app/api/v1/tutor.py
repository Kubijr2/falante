from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.repositories.grammar_repository import GrammarRepository
from app.schemas.tutor import TutorRequest, TutorResponse, TutorStatus
from app.services.ai.base import ChatMessage
from app.services.ai.factory import AIFeatureDisabledError
from app.services.tutor_service import TutorService

router = APIRouter(prefix="/tutor", tags=["tutor"])


def get_service(db: Session = Depends(get_db)) -> TutorService:
    return TutorService(GrammarRepository(db))


@router.get("/status", response_model=TutorStatus)
def get_status():
    """
    Lets the frontend check up front whether AI is configured, so it can
    show a clear "add your API key" state instead of only failing after the
    person tries to ask something.
    """
    return TutorStatus(enabled=bool(settings.ai_api_key))


@router.post("/ask", response_model=TutorResponse)
def ask_tutor(payload: TutorRequest, service: TutorService = Depends(get_service)):
    history = [ChatMessage(role=m.role, content=m.content) for m in payload.history]
    try:
        answer = service.ask(payload.question, history, payload.topic_slug)
    except AIFeatureDisabledError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)
        ) from exc
    return TutorResponse(answer=answer)
