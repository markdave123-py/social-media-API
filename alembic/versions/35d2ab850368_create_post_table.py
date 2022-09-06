"""create post table

Revision ID: 35d2ab850368
Revises: 
Create Date: 2022-09-05 19:51:58.867029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35d2ab850368' 
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable = False, primary_key = True),
                        sa.Column('title', sa.String(),nullable = False),
                        sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
