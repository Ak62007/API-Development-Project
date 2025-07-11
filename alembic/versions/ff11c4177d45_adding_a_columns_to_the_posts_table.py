"""adding a columns to the posts table

Revision ID: ff11c4177d45
Revises: eae271bc480a
Create Date: 2025-07-11 10:55:09.798393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff11c4177d45'
down_revision: Union[str, Sequence[str], None] = 'eae271bc480a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
