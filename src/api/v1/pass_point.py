import logging
from fastapi import status, APIRouter
from fastapi.responses import JSONResponse

from schemas.pass_points import PassCreate
from db import db_dependency
from services import db_post_pass


pass_router = APIRouter(prefix="/pass", tags=['pass'])

logger = logging.getLogger("pass_logger")


@pass_router.post("/pass_post")
async def post_pass(db: db_dependency, pass_data: PassCreate):
    try:
        db_pass = await db_post_pass(db, pass_data)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": 200,
                "message": "Отправлено успешно",
                "id": db_pass.id
            }
        )
    except ValueError as e:
        await db.rollback()
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": 400,
                "message": str(e),
                "id": None
            }
        )
    except Exception as e:
        await db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": 500,
                "message": f"Ошибка сервера: {str(e)}",
                "id": None
            }
        )
