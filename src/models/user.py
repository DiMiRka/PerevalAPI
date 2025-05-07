from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, UniqueConstraint

from src.models.base import Base


class User(Base):
    """Стандартная модель пользователя"""
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
