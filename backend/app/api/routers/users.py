import typing as t
from fastapi import APIRouter, Request, Depends

from app.db.session import get_db
from app.db.crud import (
    get_users,
    get_user,
    create_user,
    get_friends_from_db
)
from app.db.schemas import UserCreate, User
from app.core.auth import get_current_active_user, get_current_user

users_router = r = APIRouter()


# @r.get(
#     "/users",
#     response_model=t.List[User],
#     response_model_exclude_none=True,
# )
# async def users_list(
#     response: Response,
#     db=Depends(get_db),
#     current_user=Depends(get_current_user),
# ):
#     """
#     Get all users
#     """
#     users = get_users(db)
#     # This is necessary for react-admin to work
#     response.headers["Content-Range"] = f"0-9/{len(users)}"
#     return users


@r.get("/users/me", response_model=User, response_model_exclude_none=True)
async def user_me(current_user=Depends(get_current_user)):
    """
    Get own user
    """
    return current_user


# @r.get(
#     "/users/{user_id}",
#     response_model=User,
#     response_model_exclude_none=True,
# )
# async def user_details(
#     request: Request,
#     user_id: int,
#     db=Depends(get_db),
#     current_user=Depends(get_current_user),
# ):
#     """
#     Get any user details
#     """
#     user = get_user(db, user_id)
#     return user
#     # return encoders.jsonable_encoder(
#     #     user, skip_defaults=True, exclude_none=True,
#     # )


# @r.post("/users", response_model=User, response_model_exclude_none=True)
# async def user_create(
#     request: Request,
#     user: UserCreate,
#     db=Depends(get_db),
#     current_user=Depends(get_current_active_user),
# ):
#     """
#     Create a new user
#     """
#     return create_user(db, user)


@r.get("/getFriends", response_model=t.List[User])
async def get_friends(tags: str = '', limit: int = 25, db=Depends(get_db),
                      current_user=Depends(get_current_active_user)):
    # :TODO TAGS!!
    friends = get_friends_from_db(db, current_user.id, limit)
    res = []
    for f in friends:
        res.append(User(id=f.id, email=f.email, first_name=f.first_name, last_name=f.last_name, is_active=False))
    return res
