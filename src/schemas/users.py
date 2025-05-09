from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from email_validator import validate_email, EmailNotValidError


class UserBase(BaseModel):
    """Базовая схема для пользователя"""
    email: EmailStr = Field(..., max_length=255)
    fam: str = Field(..., max_length=50)
    name: str = Field(..., max_length=50)
    otc: Optional[str] = Field(None, max_length=50)
    phone: str = Field(..., max_length=20)

    # Валидация поля email
    @field_validator('email')
    def validate_email(cls, v: str) -> str:
        """Многоуровневая валидация email"""
        try:
            # Проверка через email-validator
            email_info = validate_email(
                v,
                check_deliverability=False,
                allow_smtputf8=False
            )
            return email_info.normalized.lower()
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email: {str(e)}")
