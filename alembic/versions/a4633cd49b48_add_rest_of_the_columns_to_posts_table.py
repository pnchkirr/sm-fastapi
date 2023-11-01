"""add rest of the columns to posts table

Revision ID: a4633cd49b48
Revises: bbb95e81f07c
Create Date: 2023-11-01 11:30:22.553367

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4633cd49b48'
down_revision: Union[str, None] = 'bbb95e81f07c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False)
                  )
    op.add_column('posts',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False)
                  )


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
