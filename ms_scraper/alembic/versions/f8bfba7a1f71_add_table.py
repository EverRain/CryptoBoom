"""add table

Revision ID: f8bfba7a1f71
Revises: 6404573fc567
Create Date: 2025-04-25 20:11:46.275634

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8bfba7a1f71'
down_revision: Union[str, None] = '6404573fc567'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('articles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('url', sa.String(length=512), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('source', sa.String(length=255), nullable=False),
    sa.Column('scraped_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('articles')
    # ### end Alembic commands ###
