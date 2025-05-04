import logging
from fastapi import APIRouter, HTTPException

from schemas import PassResponse
from schemas.pass_points import PassCreate
from db import db_dependency
from services import db_post_pass


pass_router = APIRouter(prefix="/pass", tags=['pass'])

logger = logging.getLogger("pass_logger")


@pass_router.post("/pass_post", response_model=PassResponse)
async def post_pass(db: db_dependency, pass_data: PassCreate):
    try:
        return await db_post_pass(db, pass_data)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
