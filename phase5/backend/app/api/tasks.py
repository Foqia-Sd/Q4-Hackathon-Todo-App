from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from ..core.security import get_db
from ..core.mui import get_mui_user_id
from ..schemas.task import TaskCreate, TaskUpdate, TaskInDB
from ..services import task as task_service

router = APIRouter()

from datetime import datetime

@router.get("/", response_model=List[TaskInDB])
def read_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    tags: Optional[str] = None,
    search: Optional[str] = None,
    sort: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    page: int = 1,
    page_size: int = 20,
    user_id: str = Depends(get_mui_user_id),
    db: Session = Depends(get_db)
):
    return task_service.get_tasks(
        db,
        user_id=user_id,
        status=status,
        priority=priority,
        category=category,
        tags=tags,
        search=search,
        sort=sort,
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size
    )

@router.post("/", response_model=TaskInDB)
def create_task(
    task_in: TaskCreate,
    user_id: str = Depends(get_mui_user_id),
    db: Session = Depends(get_db)
):
    return task_service.create_task(db, task_in=task_in, user_id=user_id)

@router.put("/{task_id}", response_model=TaskInDB)
def update_task(
    task_id: UUID,
    task_in: TaskUpdate,
    user_id: str = Depends(get_mui_user_id),
    db: Session = Depends(get_db)
):
    task = task_service.update_task(db, task_id=task_id, task_in=task_in, user_id=user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: UUID,
    user_id: str = Depends(get_mui_user_id),
    db: Session = Depends(get_db)
):
    success = task_service.delete_task(db, task_id=task_id, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None

@router.get("/search", response_model=List[TaskInDB])
def search_tasks(
    q: str = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    tags: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    sort: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    user_id: str = Depends(get_mui_user_id),
    db: Session = Depends(get_db)
):
    """
    Advanced search endpoint with full-text search and multi-criteria filtering
    """
    return task_service.get_tasks(
        db,
        user_id=user_id,
        status=status,
        priority=priority,
        category=category,
        tags=tags,
        search=q,
        sort=sort,
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size
    )

@router.get("/tags/autocomplete", response_model=List[str])
def autocomplete_tags(
    q: str = None,
    user_id: str = Depends(get_mui_user_id),
    db: Session = Depends(get_db)
):
    """
    Autocomplete endpoint for tags - returns tags that match the query
    """
    from sqlalchemy import text

    # Build a raw SQL query to unnest the tags array and filter
    sql_query = text("""
        SELECT DISTINCT unnest(tags) as tag
        FROM task
        WHERE user_id = :user_id
        AND tags IS NOT NULL
    """)

    params = {"user_id": user_id}

    if q:
        sql_query = text("""
            SELECT DISTINCT unnest(tags) as tag
            FROM task
            WHERE user_id = :user_id
            AND tags IS NOT NULL
            AND EXISTS (
                SELECT 1 FROM unnest(tags) AS t
                WHERE lower(t) LIKE :tag_pattern
            )
        """)
        params["tag_pattern"] = f"%{q.lower()}%"

    result = db.execute(sql_query, params)
    tags = [row.tag for row in result if q is None or q.lower() in row.tag.lower()]

    # Return up to 10 matching tags
    return sorted(list(set(tags)))[:10]
