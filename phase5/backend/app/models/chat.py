"""
Chat message model for storing conversation history between users and AI.
Following the requirements from the data model specification:
- Stores user inputs and AI responses
- Links to authenticated users
- Maintains conversation context
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SQLEnum
from datetime import datetime
import uuid

from . import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    message_type = Column(SQLEnum("user_input", "ai_response", name="chat_message_type"), nullable=False)
    content = Column(Text, nullable=False)
    intent_classification = Column(String, nullable=True)  # add_task, view_tasks, complete_task, delete_task, other
    task_operation_params = Column(String, nullable=True)  # JSON string for task parameters
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    session_id = Column(UUID(as_uuid=True), nullable=True)  # For grouping conversation sessions
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to User
    user = relationship("User", back_populates="chat_messages", foreign_keys=[user_id])

    def __repr__(self):
        return f"<ChatMessage(id={self.id}, user_id={self.user_id}, type={self.message_type})>"