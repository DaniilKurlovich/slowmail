from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status, Form

from app.db.session import get_db
from app.core import security
from app.core.auth import authenticate_user, sign_up_new_user
from app.db.schemas import Token
from app.mongo_controller.crud import reg_user

auth_router = r = APIRouter()


@r.post("/token", response_model=Token)
async def login(
        db=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = security.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@r.post("/signup")
async def signup(
        db=Depends(get_db), username: str = Form(...), password: str = Form(...), first_name: str = Form(...),
        last_name: str = Form(...)):
    user = sign_up_new_user(db, username, password, first_name, last_name)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    reg_user(user.id, '%s %s' % (user.first_name, user.last_name))
    access_token_expires = timedelta(
        minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = security.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}
