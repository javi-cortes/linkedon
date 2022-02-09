import pytest
from pydantic.error_wrappers import ValidationError
from sqlalchemy.orm import Session

from app.models import Job
from app.schemas.job import JobCreate
from app.services.job import JobService
from app.utils.service_result import ServiceResult


def test_create_job_return_service_result(job_service: JobService, job_create: JobCreate, db: Session):
    service_result = job_service.create_job(job_create)

    assert isinstance(service_result, ServiceResult)


def test_create_job_returns_job_inside_service_result(job_service: JobService, job_create: JobCreate, db: Session):
    service_result = job_service.create_job(job_create)

    assert isinstance(service_result.value, Job)


def test_create_job_missing_mandatory_fields(job_service: JobService, db: Session):
    with pytest.raises(ValidationError):
        JobCreate(
            name="Job name",
            salary=60000,
        )
