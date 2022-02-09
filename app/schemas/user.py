from typing import Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: Optional[int] = None
    full_name: Optional[str] = None
    email: Optional[str] = None

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    full_name: Optional[str] = None
    email: EmailStr = None
