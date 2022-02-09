import pytest

from app.services.job import JobCRUD
from app.services.user import UserCRUD


@pytest.fixture(scope="function")
def job_crud(db):
    return JobCRUD(db)


@pytest.fixture(scope="function")
def user_crud(db):
    return UserCRUD(db)
