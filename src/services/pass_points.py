from sqlalchemy.future import select

from db import db_dependency
from models import PassPoint, User, Coords, Images


async def db_post_coords(db: db_dependency, coords_data: dict):
    pass


async def db_post_pass(db: db_dependency, pass_data: dict):
    beauty_title = pass_data["beauty_title"]
    title = pass_data["title"]
    other_titles = pass_data["other_titles"]
    connect = pass_data["connect"]
    level_winter = pass_data["level"]["winter"]
    level_summer = pass_data["level"]["summer"]
    level_autumn = pass_data["level"]["autumn"]
    level_spring = pass_data["level"]["spring"]

    email = pass_data["user"]["email"]

    latitude = pass_data["coords"]["latitude"]
    longitude = pass_data["coords"]["longitude"]
    height = pass_data["coords"]["height"]

    data = pass_data["images"]


