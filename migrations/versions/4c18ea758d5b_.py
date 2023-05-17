"""empty message

Revision ID: 4c18ea758d5b
Revises: 1ea29c48af8c
Create Date: 2023-05-17 10:50:11.691332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c18ea758d5b'
down_revision = '1ea29c48af8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('charity', schema=None) as batch_op:
        batch_op.add_column(sa.Column('home_page_text', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('charity', schema=None) as batch_op:
        batch_op.drop_column('home_page_text')

    # ### end Alembic commands ###
