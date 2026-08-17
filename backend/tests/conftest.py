import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.grammar_seed_data import GRAMMAR_TOPICS
from app.core.verb_seed_data import IRREGULAR_VERBS, REGULAR_VERBS
from app.main import app
from app.models.grammar import GrammarTopic
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
    # The real app seeds grammar_topics via an Alembic data migration (see
    # alembic/versions/..._add_grammar_topics_table.py), which this in-memory
    # test DB bypasses entirely since it's built straight from the models.
    # Re-seed from the same source of truth here so tests see the same data.
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
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
