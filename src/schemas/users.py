from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from email_validator import validate_email, EmailNotValidError
import re


class UserBase(BaseModel):
    """Базовая схема для пользователя"""
    email: EmailStr = Field(..., max_length=255)
    phone: str = Field(..., max_length=20)
    fam: str = Field(..., max_length=50)
    name: str = Field(..., max_length=50)
    otc: Optional[str] = Field(None, max_length=50)

    @validator('email')
    def validate_email(cls, v):
        try:
            # Проверка email с помощью библиотеки email-validator
            email_info = validate_email(v, check_deliverability=False)
            return email_info.normalized
        except EmailNotValidError as e:
            raise ValueError(f"Некорректный email: {str(e)}")


