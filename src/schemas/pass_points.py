from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

from models import StatusEnum


class CoordsSchema(BaseModel):
    latitude: float
    longitude: float
    height: int


class ImageSchema(BaseModel):
    url: str = Field(..., max_length=255)
    title: Optional[str] = Field(None, max_length=100)


class PassBase(BaseModel):
    """Базовая схема для перевала"""
    beautyTitle: str = Field(..., max_length=20)
    title: str = Field(..., max_length=30)
    other_titles: Optional[str] = Field(None, max_length=50)
    connect:  Optional[str] = Field(None, max_length=50)

    coords: CoordsSchema
    images: List[ImageSchema]

    level_winter: Optional[str] = Field(None, max_length=10)
    level_summer: Optional[str] = Field(None, max_length=10)
    level_autumn: Optional[str] = Field(None, max_length=10)
    level_spring: Optional[str] = Field(None, max_length=10)

    user_email: EmailStr = Field(..., max_length=255)


class PassResponse(PassBase):
    id: int
    status: StatusEnum
    add_time: datetime
    user_email: str

