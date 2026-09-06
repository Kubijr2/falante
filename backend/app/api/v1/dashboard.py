from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.current_user import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.repositories.flashcard_repository import FlashcardRepository
from app.repositories.vocabulary_repository import VocabularyRepository
from app.schemas.dashboard import DashboardSummary
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def get_service(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> DashboardService:
    return DashboardService(
        VocabularyRepository(db, current_user.id), FlashcardRepository(db, current_user.id)
    )


@router.get("/summary", response_model=DashboardSummary)
def get_summary(service: DashboardService = Depends(get_service)):
    return service.get_summary(datetime.now(timezone.utc).date())
