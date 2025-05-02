from fastapi import APIRouter, HTTPException

from db import db_dependency
from schemas import UserBase
from services import db_crate_user


user_router = APIRouter(prefix="/user", tags=['user'])


@user_router.post("/user_create")
async def create_user(db: db_dependency, user: UserBase):
    user = user.dict()

    await db_crate_user(db, user)
