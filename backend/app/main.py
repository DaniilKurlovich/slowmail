from fastapi import FastAPI, Depends
import uvicorn

from app.api.routers.users import users_router
from app.api.routers.auth import auth_router
from app.api.routers.mail_sender import mail_routers
from app.core import config
from app.core.auth import get_current_active_user


app = FastAPI(
    title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api"
)


# @app.middleware("http")
# async def db_session_middleware(request: Request, call_next):
#     request.state.db = SessionLocal()
#     response = await call_next(request)
#     request.state.db.close()
#     return response


# Routers
app.include_router(
    users_router,
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(auth_router, tags=["auth"])
app.include_router(mail_routers, tags=["messages"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
