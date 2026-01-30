"""
Service layer for chat history management.
Handles storing and retrieving chat messages from the database.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from datetime import datetime
import uuid

from ..models.chat import ChatMessage
from ..models import User


class ChatService:
    @staticmethod
    def create_message(
        db: Session,
        user_id: uuid.UUID,
        message_type: str,
        content: str,
        intent_classification: Optional[str] = None,
        task_operation_params: Optional[str] = None,
        session_id: Optional[uuid.UUID] = None
    ) -> ChatMessage:
        """
        Create a new chat message in the database.
        """
        chat_message = ChatMessage(
            user_id=user_id,
            message_type=message_type,
            content=content,
            intent_classification=intent_classification,
            task_operation_params=task_operation_params,
            session_id=session_id,
            timestamp=datetime.utcnow()
        )

        db.add(chat_message)
        db.commit()
        db.refresh(chat_message)

        return chat_message

    @staticmethod
    def get_user_chat_history(
        db: Session,
        user_id: uuid.UUID,
        limit: int = 50,
        offset: int = 0,
        include_ai_responses: bool = True,
        include_user_inputs: bool = True
    ) -> List[ChatMessage]:
        """
        Retrieve chat history for a specific user.
        """
        query = db.query(ChatMessage).filter(ChatMessage.user_id == user_id)

        # Filter by message type if needed
        if include_ai_responses and include_user_inputs:
            # Include both types
            pass
        elif include_ai_responses:
            query = query.filter(ChatMessage.message_type == "ai_response")
        elif include_user_inputs:
            query = query.filter(ChatMessage.message_type == "user_input")
        else:
            # If neither is included, return empty list
            return []

        # Order by timestamp descending (most recent first)
        chat_history = query.order_by(desc(ChatMessage.timestamp)).offset(offset).limit(limit).all()

        return chat_history

    @staticmethod
    def get_session_chat_history(
        db: Session,
        session_id: uuid.UUID,
        limit: int = 50,
        offset: int = 0
    ) -> List[ChatMessage]:
        """
        Retrieve chat history for a specific session.
        """
        chat_history = (
            db.query(ChatMessage)
            .filter(ChatMessage.session_id == session_id)
            .order_by(desc(ChatMessage.timestamp))
            .offset(offset)
            .limit(limit)
            .all()
        )

        return chat_history

    @staticmethod
    def get_recent_conversation_context(
        db: Session,
        user_id: uuid.UUID,
        count: int = 5
    ) -> List[ChatMessage]:
        """
        Get the most recent chat messages to provide context for the AI agent.
        """
        recent_messages = (
            db.query(ChatMessage)
            .filter(ChatMessage.user_id == user_id)
            .order_by(desc(ChatMessage.timestamp))
            .limit(count)
            .all()
        )

        # Return in chronological order (oldest first)
        return list(reversed(recent_messages))

    @staticmethod
    def delete_user_chat_history(db: Session, user_id: uuid.UUID) -> int:
        """
        Delete all chat history for a user (for privacy/compliance reasons).
        Returns the number of deleted messages.
        """
        deleted_count = db.query(ChatMessage).filter(ChatMessage.user_id == user_id).delete()
        db.commit()
        return deleted_count