from .connection_manager import manager
from ..schemas.task import TaskInDB
from typing import Dict, Any

class RealtimeBroadcastService:

    @staticmethod
    async def broadcast_task_update(user_id: str, task_data: Dict[str, Any], event_type: str = "task_updated"):
        """
        Broadcast task updates to all connected clients for a specific user
        """
        message = {
            "event_type": event_type,
            "data": task_data,
            "timestamp": task_data.get("updated_at") or task_data.get("created_at")
        }

        await manager.broadcast_to_user(message, user_id)

    @staticmethod
    async def broadcast_task_created(user_id: str, task: TaskInDB):
        """
        Broadcast task creation event
        """
        task_dict = task.model_dump()
        await RealtimeBroadcastService.broadcast_task_update(
            user_id=user_id,
            task_data=task_dict,
            event_type="task_created"
        )

    @staticmethod
    async def broadcast_task_updated(user_id: str, task: TaskInDB):
        """
        Broadcast task update event
        """
        task_dict = task.model_dump()
        await RealtimeBroadcastService.broadcast_task_update(
            user_id=user_id,
            task_data=task_dict,
            event_type="task_updated"
        )

    @staticmethod
    async def broadcast_task_completed(user_id: str, task: TaskInDB):
        """
        Broadcast task completion event
        """
        task_dict = task.model_dump()
        await RealtimeBroadcastService.broadcast_task_update(
            user_id=user_id,
            task_data=task_dict,
            event_type="task_completed"
        )

    @staticmethod
    async def broadcast_task_deleted(user_id: str, task_id: str):
        """
        Broadcast task deletion event
        """
        message = {
            "event_type": "task_deleted",
            "data": {"id": task_id},
            "timestamp": None
        }

        await manager.broadcast_to_user(message, user_id)

# Global instance
broadcast_service = RealtimeBroadcastService()