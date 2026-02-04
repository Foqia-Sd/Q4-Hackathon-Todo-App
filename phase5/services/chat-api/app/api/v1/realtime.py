from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.connection_manager import manager
from app.core.config import settings
from jose import JWTError, jwt
from app.models.user import User
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter(tags=["realtime"])

async def get_current_user_ws(
    token: str = Query(...),
    db: Session = Depends(get_db)
) -> str:
    # Basic validation without db first to be fast, or with db to be safe
    # Here we just return user_id for connection manager
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return user_id
    except JWTError:
        return None

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    user_id = await get_current_user_ws(token, db)
    if not user_id:
        await websocket.close(code=1008) # Policy Violation
        return

    await manager.connect(websocket, user_id)
    try:
        while True:
            # We don't expect much input from client, but we need to keep connection open
            data = await websocket.receive_text()
            # Optional: handle client messages (e.g. ping)
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)

# Dapr subscription handler (WebHook)
@router.post("/events/task")
async def handle_task_event(request: Request):
    """
    Handle task events from Dapr Pub/Sub (task-pubsub/task-events)
    and broadcast to connected users.
    """
    try:
        # CloudEvent format
        body = await request.json()
        logger.info(f"Received event: {body}")

        # Extract data
        data = body.get("data", {})

        # In CloudEvents, the data might be nested or direct depending on content type
        # But our task_publisher sends a dict as data.

        # Extract user_id to target validation or broadcast to user
        user_id = data.get("userId")
        action = data.get("action")
        task_data = data.get("task", {})

        if user_id:
            # Send to specific user
            await manager.send_personal_message({
                "type": body.get("type", "unknown"),
                "action": action,
                "taskId": data.get("taskId"),
                "task": task_data,
                "timestamp": body.get("time", "")
            }, user_id)
            logger.info(f"Forwarded {action} event to user {user_id}")
        else:
            # Broadcast? Usually tasks are private.
            pass

        return {"status": "SUCCESS"}
    except Exception as e:
        logger.error(f"Error handling event: {e}")
        return {"status": "ERROR", "message": str(e)}

