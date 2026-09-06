from unittest.mock import patch

import pytest

from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService, InvalidGoogleTokenError


def test_unexpected_error_during_verification_becomes_invalid_token_error(db_session, monkeypatch):
    """
    Regression test: verify_oauth2_token can fail with things that aren't a
    ValueError (network errors reaching Google's cert endpoint, for
    instance). Before this was handled, that surfaced as an unhandled 500
    with no useful detail — this pins down that ANY failure here becomes a
    clean InvalidGoogleTokenError instead.
    """
    from app.core.config import settings

    monkeypatch.setattr(settings, "google_client_id", "fake-client-id")
    service = AuthService(UserRepository(db_session))

    with patch(
        "app.services.auth_service.google_id_token.verify_oauth2_token",
        side_effect=ConnectionError("could not reach Google"),
    ):
        with pytest.raises(InvalidGoogleTokenError, match="Couldn't verify with Google"):
            service.verify_google_id_token("some-token")
