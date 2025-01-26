"""Fixed relationships between models

Revision ID: d9359eb6e83e
Revises: 0dac6194485f
Create Date: 2025-01-26 14:03:29.611676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9359eb6e83e'
down_revision = '0dac6194485f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_constraint('products_report_id_fkey', type_='foreignkey')
        batch_op.drop_column('report_id')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False))

    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('report_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('products_report_id_fkey', 'reports', ['report_id'], ['id'])

    # ### end Alembic commands ###
