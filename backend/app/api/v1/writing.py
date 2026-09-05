from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.rate_limit import limiter
from app.repositories.writing_repository import WritingSubmissionRepository
from app.schemas.writing import WritingSubmissionCreate, WritingSubmissionRead
from app.services.ai.factory import AIFeatureDisabledError
from app.services.writing_coach_service import AIResponseParseError, WritingCoachService

router = APIRouter(prefix="/writing", tags=["writing"])


def get_service(db: Session = Depends(get_db)) -> WritingCoachService:
    return WritingCoachService(WritingSubmissionRepository(db))


@router.post("/review", response_model=WritingSubmissionRead, status_code=status.HTTP_201_CREATED)
@limiter.limit(lambda: f"{settings.ai_rate_limit_per_day}/day")
def review_writing(
    request: Request,  # required by slowapi to identify the caller — unused otherwise
    payload: WritingSubmissionCreate,
    service: WritingCoachService = Depends(get_service),
):
    try:
        submission = service.review(payload.text)
    except AIFeatureDisabledError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)
        ) from exc
    except AIResponseParseError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"The AI's response couldn't be understood: {exc}",
        ) from exc
    return submission


@router.get("", response_model=list[WritingSubmissionRead])
def list_submissions(limit: int = 20, service: WritingCoachService = Depends(get_service)):
    return service.list_history(limit=limit)


@router.get("/{submission_id}", response_model=WritingSubmissionRead)
def get_submission(submission_id: int, service: WritingCoachService = Depends(get_service)):
    submission = service.get_or_404(submission_id)
    if submission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Writing submission {submission_id} not found",
        )
    return submission
