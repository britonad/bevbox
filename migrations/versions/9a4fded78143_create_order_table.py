"""Create order table.

Revision ID: 9a4fded78143
Revises: 
Create Date: 2019-02-14 00:31:22.522865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a4fded78143'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('phone', sa.String(length=15), nullable=False),
    sa.Column('subscription_type', sa.String(length=10), nullable=False),
    sa.Column('city', sa.String(length=256), nullable=False),
    sa.Column('department', sa.Integer(), nullable=False),
    sa.Column('preferences', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order')
    # ### end Alembic commands ###