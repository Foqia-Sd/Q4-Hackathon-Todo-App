from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate

from sqlalchemy.orm import Session
from sqlalchemy import func, text, and_, or_
from uuid import UUID
from datetime import datetime
from typing import Optional, List

# Import the broadcast service
from .realtime_broadcast import broadcast_service
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate
from ..utils.logger import app_logger

def get_tasks(
    db: Session,
    user_id: str,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    tags: Optional[str] = None,
    search: Optional[str] = None,
    sort: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    page: int = 1,
    page_size: int = 20
) -> List[Task]:
    query = db.query(Task).filter(Task.user_id == user_id)

    # Apply filters
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if category:
        query = query.filter(Task.category.ilike(f"%{category}%"))
    if tags:
        # Filter by tags - check if any of the provided tags are in the task's tags array
        tag_list = tags.split(',')
        for tag in tag_list:
            tag_val = tag.strip()
            # Use PostgreSQL's = ANY operator to check if the tag is in the array
            query = query.filter(text(":tag_val = ANY(task.tags)")).params(tag_val=tag_val)

    # Apply search - full-text search on title and category
    if search:
        search_filter = or_(
            Task.title.ilike(f"%{search}%"),
            Task.category.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)

    # Apply date range filter
    if start_date:
        query = query.filter(Task.created_at >= start_date)
    if end_date:
        query = query.filter(Task.created_at <= end_date)

    # Apply sorting
    if sort == "priority":
        query = query.order_by(Task.priority)
    elif sort == "priority_desc":
        query = query.order_by(Task.priority.desc())
    elif sort == "due_date":
        query = query.order_by(Task.due_date)
    elif sort == "due_date_desc":
        query = query.order_by(Task.due_date.desc())
    elif sort == "created":
        query = query.order_by(Task.created_at)
    elif sort == "created_desc":
        query = query.order_by(Task.created_at.desc())
    elif sort == "title":
        query = query.order_by(Task.title)
    elif sort == "title_desc":
        query = query.order_by(Task.title.desc())
    else:
        query = query.order_by(Task.created_at.desc())  # Default sorting

    # Apply pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    return query.all()

def create_task(db: Session, task_in: TaskCreate, user_id: str) -> Task:
    app_logger.info("Creating new task", extra={"user_id": user_id, "task_title": task_in.title})

    db_obj = Task(
        **task_in.model_dump(),
        user_id=user_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    app_logger.info("Task created successfully", extra={"task_id": str(db_obj.id), "user_id": user_id})

    # Broadcast task creation to connected clients
    from ..schemas.task import TaskInDB
    task_schema = TaskInDB.from_orm(db_obj) if hasattr(TaskInDB, 'from_orm') else TaskInDB.model_validate(db_obj)
    import asyncio
    # Note: We're not awaiting this to avoid blocking the main operation
    asyncio.create_task(broadcast_service.broadcast_task_created(user_id, task_schema))

    return db_obj

def update_task(db: Session, task_id: UUID, task_in: TaskUpdate, user_id: str) -> Optional[Task]:
    app_logger.info("Updating task", extra={"task_id": str(task_id), "user_id": user_id})

    db_obj = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not db_obj:
        app_logger.warning("Task not found for update", extra={"task_id": str(task_id), "user_id": user_id})
        return None

    update_data = task_in.model_dump(exclude_unset=True)
    if not update_data: # No changes
        app_logger.info("No changes to update", extra={"task_id": str(task_id)})
        return db_obj

    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    app_logger.info("Task updated successfully", extra={"task_id": str(db_obj.id), "user_id": user_id})

    # Broadcast task update to connected clients
    from ..schemas.task import TaskInDB
    task_schema = TaskInDB.from_orm(db_obj) if hasattr(TaskInDB, 'from_orm') else TaskInDB.model_validate(db_obj)
    import asyncio
    # Note: We're not awaiting this to avoid blocking the main operation
    asyncio.create_task(broadcast_service.broadcast_task_updated(user_id, task_schema))

    return db_obj

def delete_task(db: Session, task_id: UUID, user_id: str) -> bool:
    app_logger.info("Deleting task", extra={"task_id": str(task_id), "user_id": user_id})

    db_obj = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not db_obj:
        app_logger.warning("Task not found for deletion", extra={"task_id": str(task_id), "user_id": user_id})
        return False

    # Prepare task data before deletion for broadcast
    from ..schemas.task import TaskInDB
    task_schema = TaskInDB.from_orm(db_obj) if hasattr(TaskInDB, 'from_orm') else TaskInDB.model_validate(db_obj)

    db.delete(db_obj)
    db.commit()

    app_logger.info("Task deleted successfully", extra={"task_id": str(task_id), "user_id": user_id})

    # Broadcast task deletion to connected clients
    import asyncio
    # Note: We're not awaiting this to avoid blocking the main operation
    asyncio.create_task(broadcast_service.broadcast_task_deleted(user_id, str(task_id)))

    return True

def create_task(db: Session, task_in: TaskCreate, user_id: str) -> Task:
    db_obj = Task(
        **task_in.model_dump(),
        user_id=user_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_task(db: Session, task_id: UUID, task_in: TaskUpdate, user_id: str) -> Optional[Task]:
    db_obj = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not db_obj:
        return None

    update_data = task_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_task(db: Session, task_id: UUID, user_id: str) -> bool:
    db_obj = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not db_obj:
        return False
    db.delete(db_obj)
    db.commit()
    return True
