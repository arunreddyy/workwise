"""Add email to User model

Revision ID: 0df4d7925a33
Revises: 
Create Date: 2024-12-13 10:52:44.871719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0df4d7925a33'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Step 1: Add email column as nullable
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=120), nullable=True))

    # Step 2: Populate email column with a default value for existing users
    op.execute("UPDATE user SET email = 'default@example.com'")

    # Step 3: Alter email column to make it non-nullable and unique
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('email', nullable=False)
        batch_op.create_unique_constraint('uq_user_email', ['email'])


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('uq_user_email', type_='unique')
        batch_op.drop_column('email')
