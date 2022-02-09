from typing import Optional, List

from pydantic import BaseModel


class Job(BaseModel):
    name: str
    description: Optional[str]
    country: str
    user_id: int
    salary: int = 0
    required_skills: List[str]

    class Config:
        orm_mode = True


class JobCreate(BaseModel):
    name: str
    description: str
    user_id: int
    salary: int = 0
    required_skills: List[str]
    country: str


class JobSearchCriteria(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    user_id: Optional[int] = None
    salary_max: Optional[int] = 0
    salary_min: Optional[int] = 0
    required_skills: Optional[List[str]] = None
    country: Optional[str] = None
