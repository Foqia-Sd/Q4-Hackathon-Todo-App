"""
Backend skills for AI agent to perform task operations.
These functions will be called by the AI agent to execute task operations.
They maintain separation between AI reasoning and task execution.
"""

from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
import uuid

from ..models.task import Task  # Assuming the existing Task model
from ..models.user import User  # Assuming the existing User model
from ..schemas.task import TaskCreate, TaskUpdate  # Assuming existing schemas
from .task import get_tasks, create_task, update_task, delete_task  # Import existing task functions


class TaskSkills:
    """
    Contains backend skills that the AI agent can call to perform task operations.
    Following the principle of separating reasoning (AI) from execution (skills).
    """

    @staticmethod
    def add_task_skill(
        db: Session,
        user_id: uuid.UUID,
        task_title: str,
        description: Optional[str] = None,
        due_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Skill to add a new task.
        Called by the AI agent when user wants to create a task.
        """
        try:
            # Create task using existing service
            task_data = TaskCreate(title=task_title)
            new_task = create_task(db, task_data, user_id)

            return {
                "success": True,
                "message": f"Task '{task_title}' created successfully",
                "task": {
                    "id": str(new_task.id),
                    "title": new_task.title,
                    "status": new_task.status.value if hasattr(new_task.status, 'value') else str(new_task.status),
                    "priority": new_task.priority.value if hasattr(new_task.priority, 'value') else str(new_task.priority),
                    "created_at": new_task.created_at.isoformat() if new_task.created_at else None
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to create task: {str(e)}"
            }

    @staticmethod
    def view_tasks_skill(
        db: Session,
        user_id: uuid.UUID,
        status_filter: Optional[str] = None,
        limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Skill to view user's tasks.
        Called by the AI agent when user wants to see their tasks.
        """
        try:
            # Get tasks using existing service
            tasks = get_tasks(db, user_id)

            # Apply filters if specified
            if status_filter:
                tasks = [task for task in tasks if task.status == status_filter]

            if limit:
                tasks = tasks[:limit]

            task_list = []
            for task in tasks:
                task_list.append({
                    "id": str(task.id),
                    "title": task.title,
                    "status": task.status.value if hasattr(task.status, 'value') else str(task.status),
                    "priority": task.priority.value if hasattr(task.priority, 'value') else str(task.priority),
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                })

            return {
                "success": True,
                "message": f"Retrieved {len(task_list)} tasks",
                "tasks": task_list
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to retrieve tasks: {str(e)}"
            }

    @staticmethod
    def complete_task_skill(
        db: Session,
        user_id: uuid.UUID,
        task_identifier: str
    ) -> Dict[str, Any]:
        """
        Skill to mark a task as completed.
        Called by the AI agent when user wants to complete a task.
        """
        try:
            # Find task by ID or title
            tasks = get_tasks(db, user_id)
            target_task = None

            # First try to find by ID if task_identifier looks like a UUID
            try:
                task_uuid = uuid.UUID(task_identifier)
                # We need to get the specific task by ID
                target_task = next((t for t in tasks if str(t.id) == str(task_uuid)), None)
            except ValueError:
                # If not a valid UUID, try to find by title
                for task in tasks:
                    if task_identifier.lower() in task.title.lower():
                        target_task = task
                        break

            if not target_task:
                return {
                    "success": False,
                    "message": f"No task found matching '{task_identifier}'"
                }

            # Update task status to completed
            task_update = TaskUpdate(status="completed")
            updated_task = update_task(db, target_task.id, task_update, user_id)

            return {
                "success": True,
                "message": f"Task '{updated_task.title}' marked as completed",
                "task": {
                    "id": str(updated_task.id),
                    "title": updated_task.title,
                    "status": updated_task.status
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to complete task: {str(e)}"
            }

    @staticmethod
    def delete_task_skill(
        db: Session,
        user_id: uuid.UUID,
        task_identifier: str
    ) -> Dict[str, Any]:
        """
        Skill to delete a task.
        Called by the AI agent when user wants to delete a task.
        """
        try:
            # Find task by ID or title
            tasks = get_tasks(db, user_id)
            target_task = None

            # First try to find by ID if task_identifier looks like a UUID
            try:
                task_uuid = uuid.UUID(task_identifier)
                # We need to get the specific task by ID
                target_task = next((t for t in tasks if str(t.id) == str(task_uuid)), None)
            except ValueError:
                # If not a valid UUID, try to find by title
                for task in tasks:
                    if task_identifier.lower() in task.title.lower():
                        target_task = task
                        break

            if not target_task:
                return {
                    "success": False,
                    "message": f"No task found matching '{task_identifier}'"
                }

            # Delete the task
            success = delete_task(db, target_task.id, user_id)

            if success:
                return {
                    "success": True,
                    "message": f"Task '{target_task.title}' deleted successfully"
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to delete task '{target_task.title}'"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to delete task: {str(e)}"
            }

    @staticmethod
    def search_tasks_skill(
        db: Session,
        user_id: uuid.UUID,
        search_term: str
    ) -> Dict[str, Any]:
        """
        Skill to search tasks by title or description.
        Called by the AI agent when user wants to find specific tasks.
        """
        try:
            # Get all user tasks
            tasks = TaskService.get_user_tasks(db, user_id)

            # Filter tasks based on search term
            matching_tasks = []
            for task in tasks:
                if (search_term.lower() in task.title.lower() or
                    (task.description and search_term.lower() in task.description.lower())):
                    matching_tasks.append({
                        "id": str(task.id),
                        "title": task.title,
                        "description": task.description,
                        "status": task.status,
                        "created_at": task.created_at.isoformat() if task.created_at else None
                    })

            return {
                "success": True,
                "message": f"Found {len(matching_tasks)} tasks matching '{search_term}'",
                "tasks": matching_tasks
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to search tasks: {str(e)}"
            }