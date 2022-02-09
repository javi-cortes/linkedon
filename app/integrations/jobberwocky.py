from typing import Any, List

from loguru import logger

from app.integrations.base import BaseIntegration
from app.schemas import Job


class JobberWocky(BaseIntegration):
    URL = "http://jobberwocky:8080/jobs"
    EXTERNAL_FIELDS = [
        "name",
        "salary_min",
        "salary_max",
        "country",
    ]

    def from_external_to_job_schema(self, response: Any) -> List[Job]:
        """
        Jobberwocky returns a list of jobs, lets fit those jobs in our Job
        Schema
        :param response: Jobberwocky response
        :return: List[Job]
        """
        try:
            return [
                Job(
                    name=name,
                    salary=salary,
                    country=country,
                    required_skills=required_skills,
                    user_id=0  # create an user for this external source
                )
                for name, salary, country, required_skills in response
            ]
        except TypeError:
            logger.debug(f"cannot unpack the job")
