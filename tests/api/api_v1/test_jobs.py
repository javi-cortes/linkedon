from typing import List
from unittest.mock import patch, AsyncMock

import pytest
from fastapi.testclient import TestClient
from pydantic import parse_obj_as
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas import Job
from app.schemas.job import JobCreate
from app.services.job import JobCRUD


def test_create_job(client: TestClient, db: Session):
    data = {
        "name": "is this real?",
        "description": "string",
        "user_id": 5,
        "salary": 60000,
        "required_skills": ["string"],
        "country": "string",
    }
    response = client.post(
        f"{settings.API_V1_STR}/jobs",
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]


def test_create_job_without_user(client: TestClient, db: Session):
    data = {
        "name": "is this real?",
        "description": "string",
        "salary": 0,
        "required_skills": ["string"],
        "country": "string",
    }
    response = client.post(
        f"{settings.API_V1_STR}/jobs",
        json=data,
    )
    assert response.status_code == 422


def test_create_job_with_wrong_salary(client: TestClient, db: Session):
    data = {
        "name": "is this real?",
        "description": "string",
        "user_id": 5,
        "salary": "wrong salary",
        "required_skills": ["string"],
        "country": "string",
    }
    response = client.post(
        f"{settings.API_V1_STR}/jobs",
        json=data,
    )
    assert response.status_code == 422


def test_create_job_with_missing_data(client: TestClient, db: Session):
    data = {
        "required_skills": ["string"],
        "country": "string",
    }
    response = client.post(
        f"{settings.API_V1_STR}/jobs",
        json=data,
    )
    assert response.status_code == 422


def test_create_job_empty_payload(client: TestClient, db: Session):
    response = client.post(
        f"{settings.API_V1_STR}/jobs",
        json={},
    )
    assert response.status_code == 422


def test_create_job_extra_fields(client: TestClient, db: Session):
    data = {
        "name": "is this real?",
        "description": "string",
        "user_id": 5,
        "salary": 60000,
        "required_skills": ["string"],
        "country": "string",
        "field_extra_2": "string",
        "field_extra_3": "string",
    }
    response = client.post(
        f"{settings.API_V1_STR}/jobs",
        json=data,
    )
    assert response.status_code == 200


@pytest.fixture(scope="function")
def dummy_job(client: TestClient, job_crud: JobCRUD, db: Session) -> Job:
    job_create = JobCreate(
        name="dummy job",
        description="string",
        user_id=5,
        salary=60000,
        required_skills=["string"],
        country="string",
        field_extra_2="string",
        field_extra_3="string",
    )

    return job_crud.create_job(job_create)


@patch(
    "app.services.job.JobberWocky",
    return_value=AsyncMock(retrieve_data=AsyncMock(return_value=[])),
)
def test_search_job(
    jobbermocky: AsyncMock, client: TestClient, db: Session, dummy_job: Job
):
    data = {
        "name": "dummy job",
    }
    response = client.post(
        f"{settings.API_V1_STR}/jobs/search",
        json=data,
    )
    assert response.status_code == 200
    jobs = response.json()
    assert len(jobs) > 0


@patch(
    "app.services.job.JobberWocky",
    return_value=AsyncMock(retrieve_data=AsyncMock(return_value=[])),
)
def test_search_job_non_results(
    jobbermocky: AsyncMock, client: TestClient, db: Session
):
    data = {
        "name": "not_existing_j0b!___!$$$",
    }
    response = client.post(
        f"{settings.API_V1_STR}/jobs/search",
        json=data,
    )
    assert response.status_code == 200
    jobs = response.json()
    assert not jobs


@patch(
    "app.services.job.JobberWocky",
    return_value=AsyncMock(retrieve_data=AsyncMock(return_value=[])),
)
def test_search_job_salary_max(jobbermocky: AsyncMock, client: TestClient, db: Session):
    data = {
        "salary_max": 30000,
    }
    response = client.post(
        f"{settings.API_V1_STR}/jobs/search",
        json=data,
    )
    assert response.status_code == 200
    jobs = parse_obj_as(List[Job], response.json())

    if jobs:
        assert all(job.salary < data["salary_max"] for job in jobs)


@patch(
    "app.services.job.JobberWocky",
    return_value=AsyncMock(retrieve_data=AsyncMock(return_value=[])),
)
def test_search_job_salary_min(jobbermocky: AsyncMock, client: TestClient, db: Session):
    data = {
        "salary_min": 60000,
    }
    response = client.post(
        f"{settings.API_V1_STR}/jobs/search",
        json=data,
    )
    assert response.status_code == 200
    jobs = parse_obj_as(List[Job], response.json())

    if jobs:
        assert all(job.salary > data["salary_min"] for job in jobs)

