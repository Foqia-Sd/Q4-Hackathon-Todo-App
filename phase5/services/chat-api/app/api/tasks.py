from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from ..core.security import get_db
from ..core.mui import get_mui_user_id
from ..schemas.task import TaskCreate, TaskUpdate, TaskInDB
from ..services import task as task_service

router = APIRouter()

@router.get("/", response_model=List[TaskInDB])
async def read_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    user_id: str = Depends(get_mui_user_id),
    db: Session = Depends(get_db)
):
    return await task_service.get_tasks(
        db,
        user_id=user_id,
        status=status,
        priority=priority,
        category=category,
        search=search
    )

@router.post("/", response_model=TaskInDB)
async def create_task(
    task_in: TaskCreate,
    user_id: str = Depends(get_mui_user_id),
    db: Session = Depends(get_db)
):
    return await task_service.create_task(db, task_in=task_in, user_id=user_id)

@router.put("/{task_id}", response_model=TaskInDB)
async def update_task(
    task_id: UUID,
    task_in: TaskUpdate,
    user_id: str = Depends(get_mui_user_id),
    db: Session = Depends(get_db)
):
    task = await task_service.update_task(db, task_id=task_id, task_in=task_in, user_id=user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    user_id: str = Depends(get_mui_user_id),
    db: Session = Depends(get_db)
):
    success = await task_service.delete_task(db, task_id=task_id, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None
