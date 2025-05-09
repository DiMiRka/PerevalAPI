from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, DateTime, ForeignKey, String, Enum as SQLEnum

from src.models.base import Base
from src.models.user import User


class StatusEnum(str, Enum):
    """Статус созданного перевала"""
    NEW = 'new'
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'


class Coords(Base):
    """Стандартная модель координат перевала"""
    __tablename__ = "coords"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    pass_point: Mapped["PassPoint"] = relationship("PassPoint", back_populates="coords", uselist=False)
    latitude: Mapped[float] = mapped_column()
    longitude: Mapped[float] = mapped_column()
    height: Mapped[int] = mapped_column()


class PassPoint(Base):
    """Стандартная модель перевала"""
    __tablename__ = "pereval_added"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="pass_points")

    coords_id: Mapped[int] = mapped_column(ForeignKey("coords.id"), unique=True)
    coords: Mapped["Coords"] = relationship("Coords", back_populates="pass_point")

    images: Mapped[list["Images"]] = relationship("Images", back_populates="pass_point")

    add_time = Column(DateTime(timezone=True))

    beauty_title: Mapped[str] = mapped_column(String(20), nullable=False)
    title: Mapped[str] = mapped_column(String(20), nullable=False)
    other_titles: Mapped[str] = mapped_column(String(20), nullable=False)
    connect: Mapped[str] = mapped_column(String(100))

    level_winter: Mapped[str] = mapped_column(String(10))
    level_summer: Mapped[str] = mapped_column(String(10))
    level_autumn: Mapped[str] = mapped_column(String(10))
    level_spring: Mapped[str] = mapped_column(String(10))

    @property
    def level(self):
        return {
            "winter": self.level_winter,
            "summer": self.level_summer,
            "autumn": self.level_autumn,
            "spring": self.level_spring
        }

    status: Mapped[StatusEnum] = mapped_column(
        SQLEnum(StatusEnum),
        default=StatusEnum.NEW,
        nullable=False,
        index=True
    )


class Images(Base):
    """Стандартная модель изображений перевала"""
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    pass_point_id: Mapped[int] = mapped_column(ForeignKey("pereval_added.id"))
    pass_point: Mapped["PassPoint"] = relationship("PassPoint", back_populates="images")
    data: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(100))
