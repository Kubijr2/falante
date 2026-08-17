from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.flashcard_repository import FlashcardRepository
from app.repositories.vocabulary_repository import VocabularyRepository
from app.schemas.dashboard import DashboardSummary
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def get_service(db: Session = Depends(get_db)) -> DashboardService:
    return DashboardService(VocabularyRepository(db), FlashcardRepository(db))


@router.get("/summary", response_model=DashboardSummary)
def get_summary(service: DashboardService = Depends(get_service)):
    return service.get_summary(datetime.now(timezone.utc).date())
