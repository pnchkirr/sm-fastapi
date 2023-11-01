"""add content column to posts table

Revision ID: 52c5d8338de3
Revises: 2803c1d6430f
Create Date: 2023-11-01 10:53:00.707188

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52c5d8338de3'
down_revision: Union[str, None] = '2803c1d6430f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
