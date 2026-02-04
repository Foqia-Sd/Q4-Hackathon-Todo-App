from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
from uuid import UUID

class TaskEvent(BaseModel):
    specversion: str = "1.0"
    type: str  # com.todo.task.created, etc.
    source: str = "/services/chat-api"
    id: str
    time: datetime
    datacontenttype: str = "application/json"
    data: Dict[str, Any]
