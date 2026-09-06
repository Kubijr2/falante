import os
import sqlite3
import subprocess
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent


def _run_alembic(args: list[str], db_path: Path) -> subprocess.CompletedProcess:
    env = {**os.environ, "DATABASE_URL": f"sqlite:///{db_path}"}
    return subprocess.run(
        [sys.executable, "-m", "alembic"] + args,
        cwd=BACKEND_DIR,
        env=env,
        capture_output=True,
        text=True,
    )


def test_auth_migration_succeeds_with_real_pre_existing_data(tmp_path):
    """
    Regression test for a real incident: the auth migration failed with a
    NOT NULL constraint violation on any database that already had real
    vocabulary/review/writing data (i.e. any database that had actually
    been used before this migration existed) — SQLite's batch-mode copy
    can't carry old rows forward into a new NOT NULL column with no value
    for them. This pins down that the migration now clears those specific
    tables itself rather than requiring a manual full database wipe.
    """
    db_path = tmp_path / "test.db"

    upgrade_to_pre_auth = _run_alembic(["upgrade", "f4464d2a549a"], db_path)
    assert upgrade_to_pre_auth.returncode == 0, upgrade_to_pre_auth.stderr

    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        INSERT INTO vocabulary (portuguese, english, difficulty, mastery_level, next_review_at, created_at, updated_at)
        VALUES ('falar', 'to speak', 'medium', 0, datetime('now'), datetime('now'), datetime('now'))
        """
    )
    conn.commit()
    conn.close()

    upgrade_to_head = _run_alembic(["upgrade", "head"], db_path)
    assert upgrade_to_head.returncode == 0, upgrade_to_head.stderr

    conn = sqlite3.connect(db_path)
    columns = [c[1] for c in conn.execute("PRAGMA table_info(vocabulary)").fetchall()]
    assert "user_id" in columns
    conn.close()


def test_auth_migration_recovers_from_a_partial_prior_failure(tmp_path):
    """
    Regression test for the exact broken state a real partial-failure-then-
    retry produces: the `users` table already exists (created successfully
    before a later step failed), but the other tables haven't been altered
    yet and alembic_version hasn't advanced. A naive retry crashes trying
    to recreate `users`; this migration must detect it already exists and
    continue from there instead.
    """
    db_path = tmp_path / "test.db"

    upgrade_to_pre_auth = _run_alembic(["upgrade", "f4464d2a549a"], db_path)
    assert upgrade_to_pre_auth.returncode == 0, upgrade_to_pre_auth.stderr

    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        INSERT INTO vocabulary (portuguese, english, difficulty, mastery_level, next_review_at, created_at, updated_at)
        VALUES ('falar', 'to speak', 'medium', 0, datetime('now'), datetime('now'), datetime('now'))
        """
    )
    conn.execute(
        """
        CREATE TABLE users (
            id INTEGER NOT NULL,
            email VARCHAR(320) NOT NULL,
            google_sub VARCHAR(255) NOT NULL,
            name VARCHAR(200) NOT NULL,
            picture_url VARCHAR(500),
            created_at DATETIME NOT NULL,
            PRIMARY KEY (id)
        )
        """
    )
    conn.commit()
    conn.close()

    upgrade_to_head = _run_alembic(["upgrade", "head"], db_path)
    assert upgrade_to_head.returncode == 0, upgrade_to_head.stderr


def test_auth_migration_recovers_from_a_stale_batch_mode_temp_table(tmp_path):
    """
    Regression test for a second, distinct real incident on top of the one
    above: SQLite's batch-mode alter (used to add the user_id foreign key)
    creates a `_alembic_tmp_<table>` scratch table as part of its
    copy-and-rename process. If an attempt at this migration is interrupted
    partway through that specific process (e.g. the container gets
    restarted mid-batch, which happened across a couple of real retries),
    the scratch table is left behind and the next attempt crashes trying
    to recreate it — a distinct failure mode from the `users`-already-
    exists case above, caught separately here.
    """
    db_path = tmp_path / "test.db"

    upgrade_to_pre_auth = _run_alembic(["upgrade", "f4464d2a549a"], db_path)
    assert upgrade_to_pre_auth.returncode == 0, upgrade_to_pre_auth.stderr

    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE users (
            id INTEGER NOT NULL,
            email VARCHAR(320) NOT NULL,
            google_sub VARCHAR(255) NOT NULL,
            name VARCHAR(200) NOT NULL,
            picture_url VARCHAR(500),
            created_at DATETIME NOT NULL,
            PRIMARY KEY (id)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE _alembic_tmp_flashcard_reviews (
            id INTEGER NOT NULL,
            vocabulary_id INTEGER NOT NULL,
            reviewed_at DATETIME NOT NULL,
            result VARCHAR(6) NOT NULL,
            interval_days_before INTEGER NOT NULL,
            interval_days_after INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            PRIMARY KEY (id)
        )
        """
    )
    conn.commit()
    conn.close()

    upgrade_to_head = _run_alembic(["upgrade", "head"], db_path)
    assert upgrade_to_head.returncode == 0, upgrade_to_head.stderr

    conn = sqlite3.connect(db_path)
    tables = [
        r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    ]
    assert "_alembic_tmp_flashcard_reviews" not in tables
    columns = [c[1] for c in conn.execute("PRAGMA table_info(flashcard_reviews)").fetchall()]
    assert "user_id" in columns
    conn.close()
