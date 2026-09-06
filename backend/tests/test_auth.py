from unittest.mock import patch

from app.api.v1 import auth
from app.core.security import decode_access_token
from app.main import app
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService, InvalidGoogleTokenError


def _fake_google_claims(sub="google-sub-abc", email="new@example.com", name="New User"):
    return {"sub": sub, "email": email, "name": name, "picture": "https://example.com/pic.jpg"}


def test_google_sign_in_creates_a_new_user(client, db_session):
    def override_service():
        service = AuthService(UserRepository(db_session))
        service.verify_google_id_token = lambda token: _fake_google_claims()
        return service

    app.dependency_overrides[auth.get_service] = override_service
    try:
        response = client.post("/api/v1/auth/google", json={"id_token": "fake-token"})
        assert response.status_code == 200
        body = response.json()
        assert body["user"]["email"] == "new@example.com"
        assert body["user"]["name"] == "New User"
        assert body["token_type"] == "bearer"

        decoded_user_id = decode_access_token(body["access_token"])
        assert decoded_user_id == body["user"]["id"]
    finally:
        app.dependency_overrides.pop(auth.get_service, None)


def test_google_sign_in_reuses_existing_user_on_second_login(client, db_session):
    def override_service():
        service = AuthService(UserRepository(db_session))
        service.verify_google_id_token = lambda token: _fake_google_claims(sub="same-sub")
        return service

    app.dependency_overrides[auth.get_service] = override_service
    try:
        first = client.post("/api/v1/auth/google", json={"id_token": "fake-token"})
        second = client.post("/api/v1/auth/google", json={"id_token": "fake-token"})
        assert first.json()["user"]["id"] == second.json()["user"]["id"]
    finally:
        app.dependency_overrides.pop(auth.get_service, None)


def test_google_sign_in_rejects_invalid_token(client, db_session):
    def override_service():
        service = AuthService(UserRepository(db_session))

        def raise_invalid(token):
            raise InvalidGoogleTokenError("bad token")

        service.verify_google_id_token = raise_invalid
        return service

    app.dependency_overrides[auth.get_service] = override_service
    try:
        response = client.post("/api/v1/auth/google", json={"id_token": "garbage"})
        assert response.status_code == 401
    finally:
        app.dependency_overrides.pop(auth.get_service, None)


def test_me_endpoint_requires_auth(db_session):
    from fastapi.testclient import TestClient

    from app.core.database import get_db

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as unauthenticated_client:
            response = unauthenticated_client.get("/api/v1/auth/me")
            assert response.status_code == 401
    finally:
        app.dependency_overrides.pop(get_db, None)


def test_me_endpoint_returns_current_user(client, test_user):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 200
    assert response.json()["email"] == test_user.email
