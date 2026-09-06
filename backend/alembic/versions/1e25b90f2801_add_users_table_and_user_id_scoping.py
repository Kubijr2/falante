"""add users table and user_id scoping

Revision ID: 1e25b90f2801
Revises: f4464d2a549a
Create Date: 2026-09-05 23:22:14.309297

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e25b90f2801'
down_revision: Union[str, None] = 'f4464d2a549a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = inspector.get_table_names()

    # Idempotent on purpose: SQLite's DDL isn't transactional, so if this
    # migration fails partway through (which it did in practice — see
    # below), whatever ran before the failure stays committed even though
    # Alembic doesn't consider the migration "done." Without this check, a
    # retry crashes immediately trying to recreate a table that's already
    # there, rather than picking up where it actually left off.
    if 'users' not in existing_tables:
        op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('google_sub', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('picture_url', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
        op.create_index(op.f('ix_users_google_sub'), 'users', ['google_sub'], unique=True)

    _add_user_id_column(
        inspector, 'flashcard_reviews', 'fk_flashcard_reviews_user_id_users'
    )
    _add_user_id_column(inspector, 'vocabulary', 'fk_vocabulary_user_id_users')
    _add_user_id_column(
        inspector, 'writing_submissions', 'fk_writing_submissions_user_id_users'
    )


def _add_user_id_column(inspector: sa.Inspector, table_name: str, fk_name: str) -> None:
    existing_columns = [c["name"] for c in inspector.get_columns(table_name)]
    if "user_id" in existing_columns:
        return  # already applied on a previous (partial) run of this migration

    # There's no sensible value for user_id on rows that were created before
    # accounts existed, and preserving pre-auth data wasn't required (a
    # confirmed project decision — see docs/ROADMAP.md). Clearing the table
    # first is what actually caused this migration to fail on a database
    # with any real data in it: adding user_id as NOT NULL failed while
    # SQLite's batch mode tried to copy existing rows forward, since none of
    # them have a value for the new column. Deleting first means this
    # migration succeeds regardless of what's already in the table, instead
    # of requiring anyone applying it to manually wipe their whole database
    # file beforehand.
    op.execute(f"DELETE FROM {table_name}")

    # SQLite's batch-mode alter creates a `_alembic_tmp_<table>` scratch
    # table as part of its copy-and-rename process, and cleans it up itself
    # on success. If a PREVIOUS attempt at this migration was interrupted
    # partway through that process (container killed or restarted mid-batch
    # — which is exactly what happened here across a couple of retries),
    # that scratch table is left behind, and the next attempt crashes
    # trying to recreate it. Dropping it first makes this safe to retry
    # from literally any intermediate state, not just the ones anticipated
    # above.
    op.execute(f"DROP TABLE IF EXISTS _alembic_tmp_{table_name}")

    # batch_alter_table (rather than plain add_column/create_foreign_key) is
    # required here — SQLite can't ALTER TABLE to add a foreign key
    # constraint directly, only Postgres can. Batch mode works on both: it
    # does a copy-and-rename dance under SQLite and a plain ALTER on
    # Postgres, transparently.
    with op.batch_alter_table(table_name, schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.create_index(
            batch_op.f(f'ix_{table_name}_user_id'), ['user_id'], unique=False
        )
        batch_op.create_foreign_key(fk_name, 'users', ['user_id'], ['id'])


def downgrade() -> None:
    with op.batch_alter_table('writing_submissions', schema=None) as batch_op:
        batch_op.drop_constraint('fk_writing_submissions_user_id_users', type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_writing_submissions_user_id'))
        batch_op.drop_column('user_id')

    with op.batch_alter_table('vocabulary', schema=None) as batch_op:
        batch_op.drop_constraint('fk_vocabulary_user_id_users', type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_vocabulary_user_id'))
        batch_op.drop_column('user_id')

    with op.batch_alter_table('flashcard_reviews', schema=None) as batch_op:
        batch_op.drop_constraint('fk_flashcard_reviews_user_id_users', type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_flashcard_reviews_user_id'))
        batch_op.drop_column('user_id')

    op.drop_index(op.f('ix_users_google_sub'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
