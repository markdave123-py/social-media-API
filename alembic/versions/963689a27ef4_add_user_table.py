"""add user table

Revision ID: 963689a27ef4
Revises: 35d2ab850368
Create Date: 2022-09-05 20:41:00.165029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '963689a27ef4'
down_revision = '35d2ab850368'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                            sa.Column('id', sa.Integer(),nullable = False),
                            sa.Column('email', sa.String(), nullable = False),
                            sa.Column('password', sa.String(),nullable = False),
                            sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                                        server_default = sa.text('now()'),nullable = False),
                            sa.PrimaryKeyConstraint('id'),
                            sa.UniqueConstraint('email')
                            )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
