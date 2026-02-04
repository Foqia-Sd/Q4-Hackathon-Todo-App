from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate
from ..events.task_publisher import task_publisher

async def get_tasks(
    db: Session,
    user_id: str,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort: Optional[str] = None
) -> List[Task]:
    query = db.query(Task).filter(Task.user_id == user_id)
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if category:
        query = query.filter(Task.category.ilike(f"%{category}%"))
    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))

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
    else:
        query = query.order_by(Task.created_at.desc())  # Default sorting

    return query.all()

async def create_task(db: Session, task_in: TaskCreate, user_id: str) -> Task:
    db_obj = Task(
        **task_in.model_dump(),
        user_id=user_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    # Emit event
    await task_publisher.publish_task_created(db_obj, user_id)

    return db_obj

async def update_task(db: Session, task_id: UUID, task_in: TaskUpdate, user_id: str) -> Optional[Task]:
    db_obj = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not db_obj:
        return None

    update_data = task_in.model_dump(exclude_unset=True)
    if not update_data: # No changes
        return db_obj

    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    # Emit event
    await task_publisher.publish_task_updated(db_obj, user_id, update_data)

    return db_obj

async def delete_task(db: Session, task_id: UUID, user_id: str) -> bool:
    db_obj = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not db_obj:
        return False

    db.delete(db_obj)
    db.commit()

    # Emit event
    await task_publisher.publish_task_deleted(str(task_id), user_id)

    return True
