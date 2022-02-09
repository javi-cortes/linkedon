from typing import Any, List
from urllib.parse import urlencode

import aiohttp

from app.schemas import Job
from app.schemas.job import JobSearchCriteria


class BaseIntegration(object):
    EXTERNAL_FIELDS = []
    URL = ""

    async def retrieve_data(self, job_search: JobSearchCriteria) -> List[Job]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.build_uri(job_search)) as response:
                return self.from_external_to_job_schema(await response.json())

    def from_external_to_job_schema(self, response: Any) -> List[Job]:
        """
        Convert from external format to Job Schema
        :param response:
        :return: Job Schema
        """
        pass

    def build_uri(self, job_search: JobSearchCriteria) -> str:
        job_search_dict = job_search.dict(exclude_unset=True)
        external_search_params = {
            external_field: job_search_dict.get(external_field)
            for external_field in self.EXTERNAL_FIELDS & job_search_dict.keys()
        }
        return f"{self.URL}?{urlencode(external_search_params)}"
