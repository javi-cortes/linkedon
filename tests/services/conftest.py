import pytest

from app.schemas.job import JobCreate
from app.services.job import JobService


@pytest.fixture(scope="function")
def job_service(db):
    return JobService(db)


@pytest.fixture(scope="function")
def job_create(db):
    return JobCreate(
        name="Job name",
        description="string",
        user_id=5,
        salary=60000,
        required_skills=["string"],
        country="string",
    )

