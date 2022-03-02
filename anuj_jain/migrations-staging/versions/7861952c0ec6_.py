"""empty message

Revision ID: 7861952c0ec6
Revises: c8dca2f6ca36
Create Date: 2022-03-01 04:35:22.922879

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7861952c0ec6'
down_revision = 'c8dca2f6ca36'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer_policies', sa.Column('maritial_status', sa.Boolean(), nullable=False))
    op.drop_column('customers', 'maritial_status')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customers', sa.Column('maritial_status', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.drop_column('customer_policies', 'maritial_status')
    # ### end Alembic commands ###
