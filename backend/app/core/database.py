"""
SQLAlchemy engine, session factory, and declarative base.

`connect_args` is only needed for SQLite (it disallows cross-thread use by
default, which conflicts with how FastAPI handles requests). This is the one
SQLite-specific line in the whole app — everything else is dialect-agnostic,
which is what keeps a future Postgres migration cheap.
"""
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}

engine = create_engine(settings.database_url, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency — yields a session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
