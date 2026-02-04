"""Add due_date and reminder_offset columns to tasks table

Revision ID: 002
Revises: 001
Create Date: 2026-02-02 13:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add due_date column to task table
    op.add_column('task', sa.Column('due_date', sa.DateTime(), nullable=True))

    # Add reminder_offset column to task table
    op.add_column('task', sa.Column('reminder_offset', sa.Integer(), nullable=True))


def downgrade() -> None:
    # Remove reminder_offset column from task table
    op.drop_column('task', 'reminder_offset')

    # Remove due_date column from task table
    op.drop_column('task', 'due_date')