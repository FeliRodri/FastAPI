"""add content column to posts table

Revision ID: 00bb0625a68b
Revises: 6c701da2fa75
Create Date: 2024-05-03 17:43:01.782026

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00bb0625a68b'
down_revision: Union[str, None] = '6c701da2fa75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
