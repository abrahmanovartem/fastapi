from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from models.events import Event


class User(BaseModel):
    email: EmailStr
    password: str
    events: Optional[List[Event]] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!",
                "events": [],
            }
        }


class NewUser(User):
    """Модель для регистрации: дополнительно содержит имя пользователя."""

    username: str


class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!",
            }
        }
