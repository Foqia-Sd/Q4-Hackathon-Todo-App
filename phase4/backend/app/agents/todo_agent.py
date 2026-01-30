"""
AI agent for natural language todo management.
Uses the OpenAI Agents SDK with Gemini backend (OpenAI-compatible API).
This agent handles intent recognition and delegates to backend skills for execution.
"""

import os
import logging
from typing import Dict, Any, Optional
from openai import OpenAI
from sqlalchemy.orm import Session
import uuid
import json

from ..services.task_skills import TaskSkills
from ..services.chat_service import ChatService
from ..core.config import settings

# Set up logging
logger = logging.getLogger(__name__)


class TodoAgent:
    """
    AI agent that processes natural language input and maps to todo operations.
    Uses Gemini via OpenAI-compatible API.

    Follows design requirements:
    - Stateless operation (no session memory)
    - Separation of reasoning (agent) from execution (skills)
    - Chat history stored in database
    """

    def __init__(self):
        """
        Initialize the AI agent with Gemini client (OpenAI-compatible).
        Uses GEMINI_API_KEY from environment/settings.
        """
        api_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY not set, agent will use mock responses")
            self.client = None
            self.model = None
        else:
            self.client = OpenAI(
                api_key=api_key,
                base_url=settings.GEMINI_BASE_URL
            )
            self.model = settings.GEMINI_MODEL
            logger.info(f"TodoAgent initialized with Gemini model: {self.model}")

    def process_user_input(
        self,
        db: Session,
        user_id: uuid.UUID,
        user_input: str,
        session_id: Optional[uuid.UUID] = None
    ) -> Dict[str, Any]:
        """
        Process user's natural language input and return appropriate response.
        Stateless - does NOT use session memory, each request is independent.
        Chat history is stored in database for retrieval.
        """
        try:
            # If no client (API key not set), use fallback mock implementation
            if not self.client:
                return self._process_with_mock(db, user_id, user_input, session_id)

            # Prepare the messages for the AI
            system_prompt = self._get_system_prompt()
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]

            # Call Gemini API (OpenAI-compatible) to get intent and parameters
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=512
            )

            # Parse the AI response to extract intent and parameters
            ai_content = response.choices[0].message.content
            logger.debug(f"Gemini response: {ai_content}")

            # Parse the structured response from Gemini
            parsed_args = self._parse_ai_response(ai_content, user_input)
            logger.info(f"Parsed intent: {parsed_args.get('intent')}")

            # Store user input in chat history
            ChatService.create_message(
                db=db,
                user_id=user_id,
                message_type="user_input",
                content=user_input,
                intent_classification=parsed_args.get("intent"),
                task_operation_params=json.dumps(parsed_args),
                session_id=session_id
            )

            # Execute the appropriate task skill based on intent
            result = self._execute_task_skill(db, user_id, parsed_args)

            # Generate AI response based on the result
            ai_response_content = self._generate_response(parsed_args["intent"], result)

            # Store AI response in chat history
            ai_response = ChatService.create_message(
                db=db,
                user_id=user_id,
                message_type="ai_response",
                content=ai_response_content,
                intent_classification=f"response_{parsed_args['intent']}",
                task_operation_params=json.dumps(parsed_args),
                session_id=session_id
            )

            return {
                "response": ai_response_content,
                "intent": parsed_args["intent"],
                "taskId": result.get("task", {}).get("id") if result and "task" in result else None,
                "sessionId": str(ai_response.session_id) if ai_response.session_id else str(session_id) if session_id else None,
                "taskOperationResult": result
            }

        except Exception as e:
            logger.warning(f"Gemini API error, falling back to mock: {str(e)}")
            # Fall back to mock implementation on API errors (quota, network, etc.)
            return self._process_with_mock(db, user_id, user_input, session_id)

    def _process_with_mock(
        self,
        db: Session,
        user_id: uuid.UUID,
        user_input: str,
        session_id: Optional[uuid.UUID] = None
    ) -> Dict[str, Any]:
        """
        Fallback mock implementation when Gemini API is not available.
        """
        # Simple intent classification
        parsed_args = self._mock_parse_intent(user_input)

        # Store user input
        ChatService.create_message(
            db=db,
            user_id=user_id,
            message_type="user_input",
            content=user_input,
            intent_classification=parsed_args.get("intent"),
            task_operation_params=json.dumps(parsed_args),
            session_id=session_id
        )

        # Execute task skill
        result = self._execute_task_skill(db, user_id, parsed_args)

        # Generate response
        ai_response_content = self._generate_response(parsed_args["intent"], result)

        # Store AI response
        ai_response = ChatService.create_message(
            db=db,
            user_id=user_id,
            message_type="ai_response",
            content=ai_response_content,
            intent_classification=f"response_{parsed_args['intent']}",
            session_id=session_id
        )

        return {
            "response": ai_response_content,
            "intent": parsed_args["intent"],
            "taskId": result.get("task", {}).get("id") if result and "task" in result else None,
            "sessionId": str(ai_response.session_id) if ai_response.session_id else str(session_id) if session_id else None,
            "taskOperationResult": result
        }

    def _mock_parse_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Simple mock intent parsing for when API is not available.
        """
        user_input_lower = user_input.lower().strip()

        # Helper function to extract task identifier
        def extract_identifier(text: str) -> str:
            result = text.lower()
            for phrase in ["complete", "done", "finish", "mark", "delete", "remove", "cancel",
                          "the", "task", "as", "my", "a", "an", "please", "can you", "could you"]:
                result = result.replace(phrase, "")
            return " ".join(result.split()).strip()

        if any(word in user_input_lower for word in ["add", "create", "make", "new"]):
            if "complete" in user_input_lower or "done" in user_input_lower:
                identifier = extract_identifier(user_input_lower)
                return {"intent": "complete_task", "task_identifier": identifier}
            # Extract task title by removing common phrases
            task_title = user_input_lower
            for phrase in ["add", "create", "make", "new", "task", "a", "to", "please", "can you", "could you"]:
                task_title = task_title.replace(phrase, "")
            task_title = " ".join(task_title.split()).strip()
            return {"intent": "add_task", "task_title": task_title or user_input}

        elif any(word in user_input_lower for word in ["show", "list", "display", "view", "see", "my"]):
            if "complete" in user_input_lower or "done" in user_input_lower:
                return {"intent": "view_tasks", "status_filter": "completed"}
            return {"intent": "view_tasks", "status_filter": None}

        elif any(word in user_input_lower for word in ["complete", "done", "finish", "mark"]):
            identifier = extract_identifier(user_input_lower)
            return {"intent": "complete_task", "task_identifier": identifier}

        elif any(word in user_input_lower for word in ["delete", "remove", "cancel"]):
            identifier = extract_identifier(user_input_lower)
            return {"intent": "delete_task", "task_identifier": identifier}

        elif any(word in user_input_lower for word in ["search", "find", "look"]):
            identifier = extract_identifier(user_input_lower)
            return {"intent": "search_tasks", "search_query": identifier or user_input}

        return {"intent": "other"}

    def _get_system_prompt(self) -> str:
        """
        Get the system prompt for the AI agent.
        """
        return """You are an AI assistant for a todo list application. Your role is to understand the user's natural language requests and identify what they want to do.

You must respond with a JSON object containing:
- "intent": one of ["add_task", "view_tasks", "complete_task", "delete_task", "search_tasks", "other"]
- "task_title": (for add_task) the title/name of the task to add
- "task_identifier": (for complete_task, delete_task) how to identify the task
- "search_query": (for search_tasks) what to search for
- "status_filter": (for view_tasks) "pending", "completed", or null for all

Examples:
- "add a task to buy groceries" -> {"intent": "add_task", "task_title": "buy groceries"}
- "show my tasks" -> {"intent": "view_tasks", "status_filter": null}
- "show completed tasks" -> {"intent": "view_tasks", "status_filter": "completed"}
- "complete the groceries task" -> {"intent": "complete_task", "task_identifier": "groceries"}
- "delete the meeting task" -> {"intent": "delete_task", "task_identifier": "meeting"}
- "find tasks about work" -> {"intent": "search_tasks", "search_query": "work"}

Respond ONLY with the JSON object, no other text."""

    def _parse_ai_response(self, ai_content: str, user_input: str) -> Dict[str, Any]:
        """
        Parse the AI response to extract intent and parameters.
        """
        try:
            # Try to parse as JSON
            # Clean up the response - remove markdown code blocks if present
            cleaned = ai_content.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()

            parsed = json.loads(cleaned)

            # Ensure intent is present
            if "intent" not in parsed:
                parsed["intent"] = "other"

            return parsed
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse AI response as JSON: {ai_content}")
            # Fall back to mock parsing
            return self._mock_parse_intent(user_input)

    def _execute_task_skill(self, db: Session, user_id: uuid.UUID, parsed_args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the appropriate task skill based on the parsed intent and parameters.
        """
        intent = parsed_args.get("intent")

        if intent == "add_task":
            task_title = parsed_args.get("task_title", "")
            if not task_title:
                task_title = parsed_args.get("task_identifier", "New Task")

            description = parsed_args.get("task_description")

            return TaskSkills.add_task_skill(
                db=db,
                user_id=user_id,
                task_title=task_title,
                description=description
            )

        elif intent == "view_tasks":
            status_filter = parsed_args.get("status_filter")
            if status_filter == "all":
                status_filter = None

            return TaskSkills.view_tasks_skill(
                db=db,
                user_id=user_id,
                status_filter=status_filter
            )

        elif intent == "complete_task":
            task_identifier = parsed_args.get("task_identifier") or parsed_args.get("task_title", "")

            return TaskSkills.complete_task_skill(
                db=db,
                user_id=user_id,
                task_identifier=task_identifier
            )

        elif intent == "delete_task":
            task_identifier = parsed_args.get("task_identifier") or parsed_args.get("task_title", "")

            return TaskSkills.delete_task_skill(
                db=db,
                user_id=user_id,
                task_identifier=task_identifier
            )

        elif intent == "search_tasks":
            search_query = parsed_args.get("search_query") or parsed_args.get("task_title", "")

            return TaskSkills.search_tasks_skill(
                db=db,
                user_id=user_id,
                search_term=search_query
            )

        else:
            # For 'other' intent, return a general response
            return {
                "success": True,
                "message": "I've processed your request. How else can I help you?"
            }

    def _generate_response(self, intent: str, operation_result: Dict[str, Any]) -> str:
        """
        Generate a natural language response based on the intent and operation result.
        """
        if not operation_result.get("success"):
            return f"I'm sorry, but I couldn't perform that action. {operation_result.get('message', 'An error occurred.')}"

        responses = {
            "add_task": f"I've added that task to your list! {operation_result.get('message', '')}",
            "view_tasks": f"You have {len(operation_result.get('tasks', []))} tasks in your list.",
            "complete_task": f"I've marked that task as completed! {operation_result.get('message', '')}",
            "delete_task": f"I've removed that task from your list. {operation_result.get('message', '')}",
            "search_tasks": f"I found {len(operation_result.get('tasks', []))} tasks matching your search.",
            "other": "I've processed your request. How else can I help you?"
        }

        return responses.get(intent, "I've processed your request. How else can I help you.")

    def _generate_fallback_response(self, user_input: str) -> str:
        """
        Generate a fallback response when intent parsing fails.
        """
        return f"I received your message: '{user_input}'. I'm working on improving my ability to understand requests like this. Could you try rephrasing?"


# Singleton instance for easy import
_agent_instance: Optional[TodoAgent] = None


def get_todo_agent() -> TodoAgent:
    """
    Get or create the singleton TodoAgent instance.
    """
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = TodoAgent()
    return _agent_instance
