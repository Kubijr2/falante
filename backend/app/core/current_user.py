"""
The one dependency every protected router uses. Kept separate from the
routers themselves (rather than living in, say, app/api/v1/auth.py) so any
router can import it without creating a circular import back to the auth
router.
"""
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository

_UNAUTHORIZED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Please log in to access this.",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise _UNAUTHORIZED

    token = authorization.removeprefix("Bearer ").strip()
    user_id = decode_access_token(token)
    if user_id is None:
        raise _UNAUTHORIZED

    user = UserRepository(db).get_by_id(user_id)
    if user is None:
        raise _UNAUTHORIZED

    return user
