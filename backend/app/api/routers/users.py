import typing as t
from fastapi import APIRouter, Request, Depends

from app.db.session import get_db
from app.db.crud import (
    get_users,
    get_user,
    create_user
)
from app.db.schemas import UserCreate, User
from app.core.auth import get_current_active_user, get_current_user

users_router = r = APIRouter()


@r.get("/users/me", response_model=User, response_model_exclude_none=True)
async def user_me(current_user=Depends(get_current_user)):
    """
    Get own user
    """
    return current_user
