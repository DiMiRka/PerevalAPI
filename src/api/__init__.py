from fastapi import APIRouter

from api.v1.pass_point import pass_router
from api.v1.user import user_router

api_router = APIRouter()

api_router.include_router(pass_router)
api_router.include_router(user_router)
