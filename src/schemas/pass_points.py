from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from models import StatusEnum


class CoordsSchema(BaseModel):
    """Базовая схема для координат"""
    latitude: float
    longitude: float
    height: int


class ImageSchema(BaseModel):
    """Базовая схема для изображений перевала"""
    url: str = Field(..., max_length=255)
    title: Optional[str] = None


class PassCreate(BaseModel):
    """Модель создания перевала"""
    beautyTitle: str = Field(..., max_length=20)
    title: str = Field(..., max_length=30)
    other_titles: Optional[str] = Field(None, max_length=50)
    connect: Optional[str] = Field(None, max_length=50)

    coords: CoordsSchema
    images: List[ImageSchema]
    user_id: int = Field(..., gt=0)

    level_winter: Optional[str] = None
    level_summer: Optional[str] = None
    level_autumn: Optional[str] = None
    level_spring: Optional[str] = None


class PassResponse(BaseModel):
    """Модель представления перевала"""
    id: int
    beautyTitle: str
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    coords: CoordsSchema
    images: List[ImageSchema]
    user_id: int
    add_time: datetime
    status: StatusEnum

    class Config:
        from_attributes = True
