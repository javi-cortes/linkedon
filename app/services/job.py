from typing import List

import sqlalchemy
from loguru import logger
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.integrations.jobberwocky import JobberWocky
from app.models.job import Job
from app.schemas.job import JobCreate, JobSearchCriteria
from app.services.main import AppService, AppCRUD
from app.utils.app_exceptions import AppException
from app.utils.service_result import ServiceResult


class JobService(AppService):
    def __init__(self, db: Session):
        super().__init__(db)
        self.jobberwocky = JobberWocky()

    def create_job(self, job: JobCreate) -> ServiceResult:
        new_job = JobCRUD(self.db).create_job(job)
        if not new_job:
            return ServiceResult(
                AppException.JobCreate(context={"error": "Error creating the job"})
            )
        return ServiceResult(new_job)

    async def search_jobs(self, job_search: JobSearchCriteria) -> ServiceResult:
        # here we could iterate through all the integrations to merge results
        # so far only jobberwocky
        jobberwocky_results = await self.jobberwocky.retrieve_data(job_search)
        linkedon_results = JobCRUD(self.db).get_jobs(job_search)
        # TODO: user could specify a search criteria that is not possible to
        # filter in jobberwocky, we should ensure somehow that all the
        # criteria is accomplished!

        return ServiceResult(jobberwocky_results + linkedon_results)


class JobCRUD(AppCRUD):
    def create_job(self, job_create: JobCreate) -> Job:
        """
        Persist job in the DB from the given JobCreate schema
        :param job_create:
        :return:
        """
        job = Job(**job_create.dict())
        self.db.add(job)
        try:
            self.db.commit()
            self.db.refresh(job)
        except sqlalchemy.exc.DatabaseError as error:
            logger.error(f"{error}")
            job = None
        return job

    def get_jobs(self, search_criteria: JobSearchCriteria) -> List[Job]:
        """
        Search for jobs filtering by a given search_criteria
        :param search_criteria: JobSearchCriteria
        :return: List[Job]
        """
        return (
            self.db.query(Job)
            .filter(and_(*self.build_search_query(search_criteria)))
            .all()
        )

    def build_search_query(self, search_criteria: JobSearchCriteria):
        """
        Helper to build the search query
        :param search_criteria: JobSearchCriteria
        :return: Binary queries list
        """
        search_criteria_fields = search_criteria.dict(
            exclude_unset=True, exclude_none=True
        )
        search_terms = self.get_search_terms(search_criteria)

        return [
            search_terms[field]
            for field in search_criteria_fields.keys() & search_terms.keys()
        ]

    @staticmethod
    def get_search_terms(search_criteria: JobSearchCriteria) -> dict:
        """
        Merge search_criteria terms with allowed ones to obtain all the queries
        to jobs.
        :param search_criteria: JobSearchCriteria
        :return: query dict
        """
        return {
            "name": Job.name.ilike(f"%{search_criteria.name}%"),
            "description": Job.description.ilike(f"%{search_criteria.description}%"),
            "user_id": Job.user_id == search_criteria.user_id,
            "salary_max": Job.salary <= search_criteria.salary_max,
            "salary_min": Job.salary >= search_criteria.salary_min,
            "required_skills": Job.required_skills.op("&&")(
                search_criteria.required_skills
            ),
            "country": Job.country == search_criteria.country,
        }
