from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from src.schemas.users import UserBase


class CoordsSchema(BaseModel):
    """Базовая схема для координат"""
    latitude: str
    longitude: str
    height: str


class CoordsResponse(BaseModel):
    latitude: float
    longitude: float
    height: int


class ImageSchema(BaseModel):
    """Базовая схема для изображений перевала"""
    data: str = Field(..., max_length=255)
    title: Optional[str] = None


class LevelSchema(BaseModel):
    """Базовая схема уровня сложности перевала"""
    winter: Optional[str] = None
    summer: Optional[str] = None
    autumn: Optional[str] = None
    spring: Optional[str] = None


class PassCreate(BaseModel):
    """Модель создания перевала"""
    beauty_title: str = Field(..., max_length=20)
    title: str = Field(..., max_length=30)
    other_titles: Optional[str] = Field(None, max_length=50)
    connect: Optional[str] = Field(None, max_length=50)
    add_time: Optional[datetime]
    level_winter: Optional[str] = Field(None, max_length=10)
    level_summer: Optional[str] = Field(None, max_length=10)
    level_autumn: Optional[str] = Field(None, max_length=10)
    level_spring: Optional[str] = Field(None, max_length=10)

    user: UserBase
    coords: CoordsSchema
    images: List[ImageSchema]


class PassResponse(BaseModel):
    id: int
    beauty_title: str = Field(..., max_length=20)
    title: str = Field(..., max_length=30)
    other_titles: Optional[str] = Field(None, max_length=50)
    connect: Optional[str] = Field(None, max_length=50)
    add_time: Optional[datetime]

    user: UserBase
    coords: CoordsResponse
    level: LevelSchema
    images: List[ImageSchema]
    status: Optional[str]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class PassUpdate(PassCreate):
    class Config:
        extra = "forbid"

    user: Optional[dict] = None
