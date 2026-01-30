"""
API v1 router that includes all v1 endpoints
"""
from fastapi import APIRouter
from . import chat  # Import the chat module

api_router = APIRouter()
api_router.include_router(chat.router)  # Include the chat router (prefix is handled in chat.py)