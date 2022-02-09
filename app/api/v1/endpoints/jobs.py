from typing import List

from fastapi import APIRouter, Depends
from fastapi import BackgroundTasks

from app import schemas
from app.api.deps import get_db
from app.schemas.email_sub import EmailSub
from app.schemas.job import JobCreate, JobSearchCriteria
from app.services.email_sub import EmailSubService
from app.services.job import JobService
from app.utils.service_result import handle_result

router = APIRouter()


@router.post(
    "",
    response_model=schemas.Job,
)
async def create_job(
    job: JobCreate, background_tasks: BackgroundTasks, db: get_db = Depends()
):
    """
    Submit a new job.\n
    If you want to receive alerts for new jobs use the /subscribe endpoint.
    """
    result = JobService(db).create_job(job)
    background_tasks.add_task(EmailSubService(db).new_job_created, result.value)

    return handle_result(result)


@router.post("/search", response_model=List[schemas.Job])
async def search_job(job_search_criteria: JobSearchCriteria, db: get_db = Depends()):
    """
    Search jobs with the allowed criteria.
    """
    result = await JobService(db).search_jobs(job_search_criteria)
    return handle_result(result)


@router.post("/subscribe")
async def subscribe(email_sub: EmailSub, db: get_db = Depends()):
    """
    Get alerts whenever a new job is created.\n
    You can use some parameters to apply filters.
    """
    result = await EmailSubService(db).subscribe_job_alert(email_sub)
    return handle_result(result)
