from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from ..models.task import TaskStatus, TaskPriority

class TaskBase(BaseModel):
    title: str
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    category: Optional[str] = None
    tags: Optional[List[str]] = []  # Array of tags
    due_date: Optional[datetime] = None
    reminder_offset: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date: Optional[datetime] = None
    reminder_offset: Optional[int] = None

class TaskInDB(TaskBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
