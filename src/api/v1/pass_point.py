from fastapi import APIRouter, HTTPException

from schemas import PassResponse, PassBase
from db import db_dependency

pass_router = APIRouter(prefix="/pass", tags=['pass'])


@pass_router.post("/pass_post", response_model=PassResponse)
async def post_pass(db: db_dependency, pass_data: PassBase):
    pass_data = pass_data.dict()
    print(pass_data)
    print("------------------------------")

    coords_data = pass_data.pop("coords")
    print(coords_data)

    print("------------------------------")

    images_data = pass_data.pop("images")
    print(images_data)

    print("------------------------------")

    user = pass_data.pop("user_email")
    print(user)

    print("------------------------------")

    print(pass_data)
