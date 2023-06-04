"""empty message

Revision ID: 0608a8b784ca
Revises: 0f283798e872
Create Date: 2023-05-29 03:47:59.986597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0608a8b784ca'
down_revision = '0f283798e872'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
