"""add dashboard_widgets to users

Revision ID: 5961b4e2e0b9
Revises: 1e25b90f2801
Create Date: 2026-09-06 01:07:26.972377

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5961b4e2e0b9'
down_revision: Union[str, None] = '1e25b90f2801'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Idempotent, matching the pattern established in the previous
    # migration — cheap insurance against a retry after some unrelated
    # later step in the same deploy attempt fails.
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_columns = [c["name"] for c in inspector.get_columns("users")]
    if "dashboard_widgets" not in existing_columns:
        op.add_column('users', sa.Column('dashboard_widgets', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'dashboard_widgets')
