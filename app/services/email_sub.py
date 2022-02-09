from typing import List

import sqlalchemy
from loguru import logger
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.integrations.jobberwocky import JobberWocky
from app.models.email_sub import EmailSub as EmailSubModel
from app.schemas.email_sub import EmailSub
from app.schemas.job import Job
from app.services.main import AppService, AppCRUD
from app.utils.app_exceptions import AppException
from app.utils.service_result import ServiceResult


class EmailSubService(AppService):
    def __init__(self, db: Session):
        super().__init__(db)
        self.jobberwocky = JobberWocky()

    async def subscribe_job_alert(self, email: EmailSub):
        emai_sub = EmailSubCRUD(self.db).create_job_alert_subscription(email)
        if not emai_sub:
            return ServiceResult(
                AppException.EmailSubCreate(context={"error": "Error creating sub"})
            )
        return ServiceResult(emai_sub)

    def new_job_created(self, job: Job):
        for email_sub in EmailSubCRUD(self.db).get_email_receivers(job):
            self.__fake_send_email(email_sub)

    @staticmethod
    def __fake_send_email(email_sub: EmailSubModel):
        with open("faking_email.log", "a") as f:
            f.write(f"Faking email to: {email_sub.email}")


class EmailSubCRUD(AppCRUD):
    def create_job_alert_subscription(self, email_sub: EmailSub):
        email_sub_obj = EmailSubModel(**email_sub.dict())
        self.db.add(email_sub_obj)
        try:
            self.db.commit()
            self.db.refresh(email_sub_obj)
        except sqlalchemy.exc.DatabaseError as error:
            logger.error(f"{error}")
            email_sub_obj = None
        return email_sub_obj

    def get_email_receivers(self, job: Job) -> List[EmailSubModel]:
        return (
            self.db.query(EmailSubModel)
            .filter(and_(*self.build_search_terms(job)))
            .all()
        )

    @staticmethod
    def build_search_terms(job):
        return [
            EmailSubModel.salary_max > job.salary,
            EmailSubModel.salary_min < job.salary,
        ]
