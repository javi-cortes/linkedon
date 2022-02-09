from typing import Optional

from pydantic import BaseModel, EmailStr


class EmailSub(BaseModel):
    email: EmailStr = None
    # search patterns
    salary_max: Optional[int] = 0
    salary_min: Optional[int] = 0

    class Config:
        orm_mode = True
