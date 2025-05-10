from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from sqlalchemy import update, delete

from src.db import db_dependency
from src.models import PassPoint, Coords, Images, User, StatusEnum
from src.schemas.pass_points import PassCreate, PassUpdate


async def db_post_pass(db: db_dependency, pass_data: PassCreate):
    """Добавляем перевал с координатами и изображениями в базу данных"""

    # Создаем пользователя
    db_user = User(**pass_data.user.dict())
    db.add(db_user)
    await db.flush()

    # Создаем координаты
    coords_data = {
        "latitude": float(pass_data.coords.latitude),
        "longitude": float(pass_data.coords.longitude),
        "height": int(pass_data.coords.height)
    }
    db_coords = Coords(**coords_data)
    db.add(db_coords)
    await db.flush()

    #  Разбираем уровни сложности перевала
    level = pass_data.level.dict()

    # Создаем перевал
    db_pass = PassPoint(
        **pass_data.dict(exclude={'user', 'coords', 'level', 'images'}),
        user_id=db_user.id,
        coords_id=db_coords.id,
        status=StatusEnum.NEW,
        level_winter=level["winter"],
        level_summer=level["summer"],
        level_autumn=level["autumn"],
        level_spring=level["spring"],
    )
    db.add(db_pass)
    await db.flush()

    # Создаем изображения
    db_images = [Images(**img.dict(), pass_point_id=db_pass.id) for img in pass_data.images]
    db.add_all(db_images)

    await db.commit()
    await db.refresh(db_pass)

    return db_pass


async def db_get_pass(db: db_dependency, pass_id: int):
    """Получаем перевал из базы данных по его id"""
    query = (
            select(PassPoint)
            .where(PassPoint.id == pass_id)
            .options(
                selectinload(PassPoint.user),
                selectinload(PassPoint.coords),
                selectinload(PassPoint.images),
            )
    )
    result = await db.execute(query)
    pass_point = result.scalars().first()
    return pass_point


async def db_patch_pass(db: db_dependency, pass_point: PassPoint, update_data: PassUpdate):
    """Вносим изменения существующего перевала в базе данных"""
    try:
        #  Обновляем координаты (если они есть в update_data)
        if update_data.coords:
            coords_data = {
                "latitude": float(update_data.coords.latitude),
                "longitude": float(update_data.coords.longitude),
                "height": int(update_data.coords.height)
            }
            await db.execute(
                update(Coords)
                .where(Coords.id == pass_point.coords_id)
                .values(**coords_data)
            )

        #  Обновляем основные данные перевала (исключаем user, coords, level, images)
        pass_data = update_data.dict(exclude={'user', 'coords', 'level', 'images'})
        if pass_data:
            await db.execute(
                update(PassPoint)
                .where(PassPoint.id == pass_point.id)
                .values(**pass_data)
            )

        #  Обновляем изображения (если они есть в update_data)
        if update_data.images:
            #  Удаляем старые изображения
            await db.execute(delete(Images).where(Images.pass_point_id == pass_point.id))
            db_images = [
                Images(**img.dict(), pass_point_id=pass_point.id)
                for img in update_data.images
            ]
            db.add_all(db_images)

        await db.commit()

        return {
            "state": 1,
            "message": "Успешно обновлен"
        }

    except Exception as e:
        return {
            "state": 0,
            "message": f"Ошибка сервера: {str(e)}"
        }


async def get_passes_email(db: db_dependency, email: str):
    query = (
        select(PassPoint)
        .where(User.email == email)
        .options(
            selectinload(PassPoint.user),
            selectinload(PassPoint.coords),
            selectinload(PassPoint.images),
        )
    )
    result = await db.execute(query)
    return result.scalars().all()
