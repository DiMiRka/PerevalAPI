from fastapi import APIRouter

from src.core import db_dependency
from src.schemas import UserBase
from src.services import db_create_user


user_router = APIRouter(prefix="/user", tags=['user'])


@user_router.post("/user_create")
async def create_user(db: db_dependency, user: UserBase):
    user = user.dict()

    await db_create_user(db, user)
    return f"User create: {user}"
