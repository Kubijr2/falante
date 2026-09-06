from app.core.config import Settings


def test_unrecognized_env_file_key_does_not_crash_settings(tmp_path, monkeypatch):
    """
    Regression test for a real incident: pydantic-settings enforces
    extra="forbid" by default specifically for values loaded from an actual
    .env FILE (not for plain OS environment variables — the two behave
    differently, which is what made this easy to miss in earlier testing).
    A single mistyped variable in .env — even one nobody's code reads —
    must not take the whole backend down.

    Deliberately instantiates a fresh Settings() rather than touching the
    shared app.core.config.settings singleton or reloading the module —
    both would risk leaking state into other tests that import that same
    singleton (e.g. the rate-limiting tests, which monkeypatch attributes
    on it directly).
    """
    env_file = tmp_path / ".env"
    # The exact typo that caused the real crash: "secrect" instead of "secret".
    env_file.write_text("google_client_secrect=some-value\nanother_bogus_key=whatever\n")

    monkeypatch.chdir(tmp_path)
    settings = Settings()

    assert settings.database_url  # just needs to have loaded successfully
