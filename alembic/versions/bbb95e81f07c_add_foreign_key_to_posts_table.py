"""add foreign key to posts table

Revision ID: bbb95e81f07c
Revises: 612d741f167e
Create Date: 2023-11-01 11:17:36.309172

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bbb95e81f07c'
down_revision: Union[str, None] = '612d741f167e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('user_id', sa.Integer(), nullable=False)
                  )
    op.create_foreign_key('posts_users_fk',
                          source_table='posts',
                          referent_table='users',
                          local_cols=['user_id'],
                          remote_cols=['id'],
                          ondelete='CASCADE')

def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
