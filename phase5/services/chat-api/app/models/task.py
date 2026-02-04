from sqlalchemy import Column, String, Enum, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from .base import Base, TimestampMixin

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(Base, TimestampMixin):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    title = Column(String, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    category = Column(String, nullable=True)
    recurrence_rule = Column(String, nullable=True)  # RRULE string for recurring tasks
    due_date = Column(DateTime, nullable=True)  # Due date for the task
    reminder_offset = Column(Integer, nullable=True)  # Minutes before due date to remind

    owner = relationship("User", backref="tasks")
