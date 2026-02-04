"""Add recurrence_rule column to tasks table

Revision ID: 001
Revises:
Create Date: 2026-02-02 12:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add recurrence_rule column to task table
    op.add_column('task', sa.Column('recurrence_rule', sa.String(), nullable=True))


def downgrade() -> None:
    # Remove recurrence_rule column from task table
    op.drop_column('task', 'recurrence_rule')