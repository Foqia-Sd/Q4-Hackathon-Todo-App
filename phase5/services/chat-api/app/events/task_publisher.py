import os
import json
import logging
from datetime import datetime
from uuid import uuid4
from dapr.clients import DaprClient
from .types import TaskEvent
from ..models.task import Task
from ..schemas.task import TaskInDB

logger = logging.getLogger(__name__)

PUBSUB_NAME = "task-pubsub"
TOPIC_NAME = "task-events"

class TaskPublisher:
    def __init__(self):
        self.source = "/services/chat-api"

    def _create_event(self, event_type: str, data: dict) -> TaskEvent:
        return TaskEvent(
            id=str(uuid4()),
            type=event_type,
            source=self.source,
            time=datetime.utcnow(),
            data=data
        )

    async def publish(self, event_type: str, data: dict):
        event = self._create_event(event_type, data)
        try:
            with DaprClient() as d:
                d.publish_event(
                    pubsub_name=PUBSUB_NAME,
                    topic_name=TOPIC_NAME,
                    data=event.json(),
                    data_content_type="application/cloudevents+json"
                )
                logger.info(f"Published event {event_type} id={event.id}")
        except Exception as e:
            logger.error(f"Failed to publish event {event_type}: {str(e)}")
            # In production, you might want to implement a fallback (e.g., local queue)

    async def publish_task_created(self, task: Task, user_id: str):
        task_schema = TaskInDB.model_validate(task)
        payload = {
            "taskId": str(task.id),
            "userId": str(user_id),
            "action": "CREATED",
            "task": task_schema.model_dump(mode='json')
        }
        await self.publish("com.todo.task.created", payload)

    async def publish_task_updated(self, task: Task, user_id: str, changes: dict):
        task_schema = TaskInDB.model_validate(task)
        payload = {
            "taskId": str(task.id),
            "userId": str(user_id),
            "action": "UPDATED",
            "task": task_schema.model_dump(mode='json'),
            "changes": changes
        }
        await self.publish("com.todo.task.updated", payload)

    async def publish_task_completed(self, task: Task, user_id: str):
        task_schema = TaskInDB.model_validate(task)
        payload = {
            "taskId": str(task.id),
            "userId": str(user_id),
            "action": "COMPLETED",
            "task": task_schema.model_dump(mode='json')
        }
        await self.publish("com.todo.task.completed", payload)

    async def publish_task_deleted(self, task_id: str, user_id: str):
        payload = {
            "taskId": str(task_id),
            "userId": str(user_id),
            "action": "DELETED"
        }
        await self.publish("com.todo.task.deleted", payload)

task_publisher = TaskPublisher()
