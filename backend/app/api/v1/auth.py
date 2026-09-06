from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.current_user import get_current_user
from app.core.database import get_db
from app.core.security import create_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AuthResponse, GoogleAuthRequest, UserRead
from app.services.auth_service import AuthService, InvalidGoogleTokenError

router = APIRouter(prefix="/auth", tags=["auth"])


def get_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))


@router.post("/google", response_model=AuthResponse)
def google_sign_in(payload: GoogleAuthRequest, service: AuthService = Depends(get_service)):
    try:
        claims = service.verify_google_id_token(payload.id_token)
    except InvalidGoogleTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    user = service.get_or_create_user(claims)
    access_token = create_access_token(user.id)
    return AuthResponse(access_token=access_token, user=UserRead.model_validate(user))


@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    """Lets the frontend re-hydrate auth state on load (confirms a stored token is still valid)."""
    return current_user
