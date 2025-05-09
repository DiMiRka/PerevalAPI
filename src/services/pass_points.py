from sqlalchemy.orm import selectinload
from sqlalchemy.future import select

from src.db import db_dependency
from src.models import PassPoint, Coords, Images, User, StatusEnum
from src.schemas.pass_points import PassCreate


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
