from fastapi import APIRouter, HTTPException

pass_router = APIRouter(prefix="/pass", tags=['pass'])


@pass_router.post("/pass_post")
async def post_pass():
    pass
