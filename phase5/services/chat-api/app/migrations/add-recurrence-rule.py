"""
Migration to add recurrence_rule column to tasks table
"""
import asyncio
from sqlalchemy import Column, String, MetaData, Table, create_engine
from sqlalchemy.dialects.postgresql import UUID

# Database URL - this should match your configuration
DATABASE_URL = "postgresql://user:password@localhost/todo_chatbot"

def migrate():
    # Create engine
    engine = create_engine(DATABASE_URL)

    # Define the tasks table structure
    metadata = MetaData()
    tasks_table = Table('task', metadata,
        autoload=True,
        autoload_with=engine
    )

    # Check if the column already exists
    if 'recurrence_rule' not in [col.name for col in tasks_table.columns]:
        # Add the recurrence_rule column
        with engine.connect() as conn:
            conn.execute("ALTER TABLE task ADD COLUMN recurrence_rule VARCHAR;")
            conn.commit()
            print("Added recurrence_rule column to task table")
    else:
        print("recurrence_rule column already exists")

if __name__ == "__main__":
    migrate()