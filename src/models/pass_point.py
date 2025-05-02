from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from decimal import Decimal

Base = declarative_base()


class PassPoint(Base):
    __tablename__ = "pereval_added"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="pass_points")
    coords_id: Mapped[int] = mapped_column(ForeignKey("coords.id"), unique=True)
    add_time: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    beautyTitle: Mapped[str] = mapped_column(String(20), nullable=False)
    title: Mapped[str] = mapped_column(String(20), nullable=False)
    other_titles: Mapped[str] = mapped_column(String(20), nullable=False)
    connect: Mapped[str] = mapped_column(String(100))


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    pass_points: Mapped[list["PassPoint"]] = relationship("PassPoint", back_populates="user")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    phone: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    fam: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    otc: Mapped[str] = mapped_column(String(50))
    __table_args__ = (
        UniqueConstraint('email', name='uq_user_email'),
        UniqueConstraint('phone', name='uq_user_phone'),
    )


class Coords(Base):
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    pass_point: Mapped["PassPoint"] = relationship("PassPoint", back_populates="coords", uselist=False)
    latitude: Mapped[float] = mapped_column()
    longitude: Mapped[float] = mapped_column()
    height: Mapped[int] = mapped_column()
