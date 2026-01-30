from fastapi import Depends
from ..models.user import User
from .security import get_current_active_user

async def get_mui_user_id(
    current_user: User = Depends(get_current_active_user)
) -> str:
    """
    Centralized dependency for Multi-User Isolation (MUI).
    Returns the user_id of the authenticated user to be used in all task filters.
    """
    return str(current_user.id)
