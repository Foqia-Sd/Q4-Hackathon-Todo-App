from fastapi import WebSocket
from typing import List
from ..services.connection_manager import manager
import jwt
from ..core.config import settings

async def websocket_endpoint(websocket: WebSocket, token: str):
    # Decode the token to get user_id
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            await websocket.close(code=1008, reason="Invalid token")
            return
    except jwt.ExpiredSignatureError:
        await websocket.close(code=1008, reason="Token expired")
        return
    except jwt.JWTError:
        await websocket.close(code=1008, reason="Invalid token")
        return

    await manager.connect(websocket, user_id)
    try:
        while True:
            # Listen for messages (optional - for bidirectional communication)
            data = await websocket.receive_text()
            # Process incoming messages if needed - for now just echo back
            await websocket.send_text(f"Message received: {data}")
    except Exception:
        manager.disconnect(websocket, user_id)