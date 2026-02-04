"""Add priority column to tasks table

Revision ID: 003
Revises: 002
Create Date: 2026-02-03 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create the task_priority enum type
    task_priority_enum = postgresql.ENUM('LOW', 'MEDIUM', 'HIGH', name='taskpriority')
    task_priority_enum.create(op.get_bind(), checkfirst=True)

    # Add priority column to task table
    op.add_column('task', sa.Column('priority', task_priority_enum, server_default='MEDIUM', nullable=False))


def downgrade() -> None:
    # Remove priority column from task table
    op.drop_column('task', 'priority')

    # Drop the task_priority enum type
    task_priority_enum = postgresql.ENUM('LOW', 'MEDIUM', 'HIGH', name='taskpriority')
    task_priority_enum.drop(op.get_bind(), checkfirst=True)