"""add last few columns to post table

Revision ID: b30ffceb091b
Revises: 018ceb1a3c5b
Create Date: 2022-09-05 22:19:43.303776

"""
from http import server
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b30ffceb091b'
down_revision = '018ceb1a3c5b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable = False, server_default = 'TRUE'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone= True), 
                                            server_default = sa.text('now()'), nullable = False),)
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
