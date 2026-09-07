from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.current_user import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.repositories.flashcard_repository import FlashcardRepository
from app.repositories.vocabulary_repository import VocabularyRepository
from app.repositories.writing_repository import WritingSubmissionRepository
from app.schemas.analytics import AnalyticsSummary
from app.services.analytics_service import AnalyticsService, InvalidRangeError

router = APIRouter(prefix="/analytics", tags=["analytics"])


def get_service(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> AnalyticsService:
    return AnalyticsService(
        VocabularyRepository(db, current_user.id),
        FlashcardRepository(db, current_user.id),
        WritingSubmissionRepository(db, current_user.id),
    )


@router.get("/summary", response_model=AnalyticsSummary)
def get_summary(range: str = "30d", service: AnalyticsService = Depends(get_service)):
    try:
        return service.get_summary(range)
    except InvalidRangeError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)
        ) from exc
