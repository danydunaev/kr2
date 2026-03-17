from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import re


# ===== Задание 3.1 =====
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None
    is_subscribed: Optional[bool] = False

    @field_validator("age")
    @classmethod
    def validate_age(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Возраст должен быть положительным")
        return v


# ===== Задание 5.1–5.3 =====
class LoginRequest(BaseModel):
    """Модель для запроса логина"""
    username: str
    password: str


# ===== Задание 5.5 =====
class CommonHeaders(BaseModel):
    user_agent: str
    accept_language: str

    @field_validator("accept_language")
    @classmethod
    def validate_language(cls, v):
        # Более гибкий паттерн для Accept-Language
        pattern = r'^[a-zA-Z-]+(?:;[a-zA-Z]=[0-9.]+)?(?:,[a-zA-Z-]+(?:;[a-zA-Z]=[0-9.]+)?)*$'
        if not re.match(pattern, v):
            raise ValueError("Неверный формат Accept-Language")
        return v