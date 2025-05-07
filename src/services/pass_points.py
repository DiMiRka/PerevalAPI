from datetime import datetime
from fastapi import HTTPException

from src.db import db_dependency
from src.models import PassPoint, Coords, Images, User, StatusEnum
from src.schemas import PassResponse
from src.schemas.pass_points import PassCreate


async def db_post_pass(db: db_dependency, pass_data: PassCreate):
    """Добавляем перевал с координатами и изображениями в базу данных"""

    # Проверяем существование пользователя
    user = await db.get(User, pass_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Создаем координаты
    db_coords = Coords(**pass_data.coords.dict())
    db.add(db_coords)
    await db.flush()

    # Создаем перевал
    db_pass = PassPoint(
        **pass_data.dict(exclude={'coords', 'images'}),
        coords_id=db_coords.id,
        status=StatusEnum.NEW,
        add_time=datetime.utcnow()
    )
    db.add(db_pass)
    await db.flush()

    # Создаем изображения
    db_images = [Images(**img.dict(), pass_point_id=db_pass.id) for img in pass_data.images]
    db.add_all(db_images)

    await db.commit()
    await db.refresh(db_pass)

    # Формируем ответ
    return PassResponse(
        id=db_pass.id,
        beautyTitle=db_pass.beautyTitle,
        title=db_pass.title,
        other_titles=db_pass.other_titles,
        connect=db_pass.connect,
        coords=pass_data.coords,
        images=pass_data.images,
        user_id=pass_data.user_id,
        add_time=db_pass.add_time,
        status=db_pass.status,
        level_winter=db_pass.level_winter,
        level_summer=db_pass.level_summer,
        level_autumn=db_pass.level_autumn,
        level_spring=db_pass.level_spring
    )
