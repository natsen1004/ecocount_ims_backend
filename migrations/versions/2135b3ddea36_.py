"""empty message

Revision ID: 2135b3ddea36
Revises: 0da8d406e1db
Create Date: 2025-02-03 14:22:48.390431

"""
from alembic import op
import sqlalchemy as sa
from werkzeug.security import generate_password_hash

default_password_hash = generate_password_hash("defaultpassword", method="pbkdf2:sha256")
# revision identifiers, used by Alembic.
revision = '2135b3ddea36'
down_revision = '0da8d406e1db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(), nullable=False, server_default=default_password_hash))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###
