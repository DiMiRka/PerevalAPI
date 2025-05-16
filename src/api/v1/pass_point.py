import logging
from fastapi import status, APIRouter, HTTPException
from fastapi.responses import JSONResponse

from src.schemas.pass_points import PassCreate, PassResponse, PassUpdate
from src.core import db_dependency
from src.services import db_post_pass, db_get_pass, db_patch_pass, db_get_passes_email


pass_router = APIRouter(prefix="/pass", tags=['pass'])

logger = logging.getLogger("pass_logger")


@pass_router.post("/pass_post", summary="Добавить новый перевал",
                  description="Создает новую запись о перевале с данными пользователя, координатами и изображениями")
async def post_pass(db: db_dependency, pass_data: PassCreate):
    """Создать новый перевал"""
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


@pass_router.get("/pass_get/", response_model=PassResponse,
                 summary="Получить перевал по его id",
                 description="Получить запись о перевале с данными пользователя, координатами и изображениями")
async def get_pass(db: db_dependency, pass_id: int):
    """Получить перевал по его id"""
    try:
        db_pass = await db_get_pass(db, int(pass_id))
        if not db_pass:
            raise HTTPException(status_code=404, detail="Pereval not found")

        return db_pass

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


@pass_router.patch("/pass_patch/", summary="Изменить данные перевала",
                   description="При статусе перевала 'new' изменить запись о перевале, включая координаты и изображения")
async def patch_pass(db: db_dependency, pass_id: int, update_data: PassUpdate):
    """Внести изменения в созданный перевал"""
    try:
        db_pass = await db_get_pass(db, pass_id)

        if not db_pass:
            raise HTTPException(status_code=404, detail="Pereval not found")

        if db_pass.status != "new":
            raise HTTPException(status_code=404, detail="The pass does not have the 'new'")

        content = await db_patch_pass(db, db_pass, update_data)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=content
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


@pass_router.get("/pass_get_email/", response_model=list[PassResponse],
                 summary="Получить все перевалы пользователя по его email",
                 description="Получить список перевалов, созданные пользователем, включая "
                             "координаты, картинки и данные пользователя")
async def get_passes_email(db: db_dependency, email: str):
    """Получить все перевалы по email юзера"""
    try:
        passes = await db_get_passes_email(db, email)

        if not passes:
            raise HTTPException(status_code=404, detail=f"No found for email {email}")

        return passes

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
