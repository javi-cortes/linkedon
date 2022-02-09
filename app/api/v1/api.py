from fastapi import APIRouter

from app.api.v1.endpoints import jobs, user

api_router = APIRouter()
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(user.router, prefix="/users", tags=["users"])


tags_metadata = [
    {
        "name": "jobs",
        "description": "Submit, search and subscribe to new jobs.",
    },
    {
        "name": "users",
        "description": "Operations with users",
    },
]
