from fastapi import APIRouter

from src.api.v1.pass_point import pass_router

api_router = APIRouter()

api_router.include_router(pass_router)
