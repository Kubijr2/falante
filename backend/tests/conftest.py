import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.current_user import get_current_user
from app.core.database import Base, get_db
from app.core.grammar_seed_data import GRAMMAR_TOPICS
from app.core.verb_seed_data import IRREGULAR_VERBS, REGULAR_VERBS
from app.main import app
from app.models.grammar import GrammarTopic
from app.models.user import User
from app.models.verb import Verb


@pytest.fixture()
def db_session():
    """Fresh in-memory SQLite DB for every test — fully isolated, no shared state."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    session.add_all(GrammarTopic(**topic) for topic in GRAMMAR_TOPICS)
    session.add_all(
        Verb(infinitive=v["infinitive"], translation=v["translation"], is_irregular=False)
        for v in REGULAR_VERBS
    )
    session.add_all(
        Verb(
            infinitive=v["infinitive"],
            translation=v["translation"],
            is_irregular=True,
            irregular_conjugations=json.dumps(v["conjugations"]),
        )
        for v in IRREGULAR_VERBS
    )
    session.commit()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def test_user(db_session) -> User:
    """The default logged-in user for any test using the `client` fixture."""
    user = User(email="test@example.com", google_sub="test-google-sub-1", name="Test User")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture()
def second_user(db_session) -> User:
    """A distinct user, for tests that specifically verify data isolation between accounts."""
    user = User(email="other@example.com", google_sub="test-google-sub-2", name="Other User")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture()
def client(db_session, test_user):
    """
    A TestClient already "logged in" as `test_user` by default — every
    existing test written before auth existed keeps working unmodified,
    since protected routes see a real authenticated user without each test
    needing to construct a token. Tests that specifically need a *different*
    or *no* user override app.dependency_overrides[get_current_user]
    themselves, same pattern as overriding get_service elsewhere.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    def override_get_current_user():
        return test_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
