"""
Chat API endpoint for AI-powered natural language interaction.
Stateless endpoint that accepts user input and returns AI response.
Chat history is stored in database but NOT used for session memory.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
import uuid
import logging

from app.core.database import get_db
from app.models.user import User
from app.core.security import get_current_user
from app.services.chat_service import ChatService
from app.agents.todo_agent import get_todo_agent

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
async def process_chat_input(
    request: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Process natural language input and return AI response.
    Stateless operation - does NOT use session memory.
    Chat history is stored in database for retrieval but not for context.
    """
    # Validation
    message = request.get("message")
    if not message or not isinstance(message, str) or len(message.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message is required and must be a non-empty string"
        )

    # Validate message length
    if len(message) > 2000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message is too long. Maximum length is 2000 characters."
        )

    # Validate session_id if provided (optional, for grouping)
    session_id_str = request.get("sessionId")
    session_id = None
    if session_id_str:
        if not isinstance(session_id_str, str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session ID must be a string if provided"
            )
        try:
            session_id = uuid.UUID(session_id_str)
        except ValueError:
            # If invalid UUID, generate a new one
            session_id = uuid.uuid4()

    try:
        # Get the TodoAgent instance
        agent = get_todo_agent()

        # Process the user input through the agent
        # Note: includeHistory is ignored - we operate statelessly
        result = agent.process_user_input(
            db=db,
            user_id=current_user.id,
            user_input=message.strip(),
            session_id=session_id
        )

        logger.info(f"Processed chat for user {current_user.id}, intent: {result.get('intent')}")

        # Add suggestions for follow-up actions
        suggestions = []
        intent = result.get("intent", "other")
        if intent in ["add_task", "complete_task", "delete_task"]:
            suggestions.extend([
                "Would you like to add another task?",
                "Do you want to see your task list?"
            ])
        elif intent.startswith("view") or intent == "search_tasks":
            suggestions.extend([
                "Would you like to add a new task?",
                "Do you want to mark any tasks as completed?"
            ])

        if suggestions:
            result["suggestions"] = suggestions[:2]

        return result

    except Exception as e:
        logger.error(f"Error processing chat input: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing your message. Please try again."
        )


@router.get("/history")
async def get_chat_history(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve chat history for the current user.
    Returns messages in reverse chronological order (most recent first).
    """
    try:
        history = ChatService.get_user_chat_history(
            db=db,
            user_id=current_user.id,
            limit=limit,
            offset=offset
        )

        # Convert to response format
        response = []
        for msg in history:
            response.append({
                "id": str(msg.id),
                "user_id": str(msg.user_id),
                "message_type": msg.message_type,
                "content": msg.content,
                "intent_classification": msg.intent_classification,
                "task_operation_params": msg.task_operation_params,
                "timestamp": msg.timestamp.isoformat() if msg.timestamp else None,
                "session_id": str(msg.session_id) if msg.session_id else None
            })

        return response

    except Exception as e:
        logger.error(f"Error fetching chat history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving chat history"
        )


@router.delete("/history")
async def delete_chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete all chat history for the current user.
    """
    try:
        deleted_count = ChatService.delete_user_chat_history(
            db=db,
            user_id=current_user.id
        )

        return {
            "success": True,
            "message": f"Deleted {deleted_count} messages",
            "deleted_count": deleted_count
        }

    except Exception as e:
        logger.error(f"Error deleting chat history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting chat history"
        )
