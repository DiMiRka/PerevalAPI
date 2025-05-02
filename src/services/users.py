from db import db_dependency
from models import User


async def db_crate_user(db: db_dependency, user: dict):
    """Added user to database"""
    email = user["email"]
    phone = user["phone"]
    fam = user["fam"]
    name = user["name"]
    otc = user["otc"]
    db_user = User(email=email, phone=phone, fam=fam, name=name, otc=otc)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
