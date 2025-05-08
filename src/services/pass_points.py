from datetime import datetime
from fastapi import HTTPException

from src.db import db_dependency
from src.models import PassPoint, Coords, Images, User, StatusEnum
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

    return db_pass
