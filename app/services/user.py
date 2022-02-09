import sqlalchemy
from loguru import logger

from app.models.user import User
from app.schemas.user import UserCreate
from app.services.main import AppService, AppCRUD
from app.utils.app_exceptions import AppException
from app.utils.service_result import ServiceResult


class UserService(AppService):
    def create_user(self, user: UserCreate) -> ServiceResult:
        new_user = UserCRUD(self.db).create_user(user)
        if not new_user:
            return ServiceResult(AppException.UserCreate(
                context={"error": "Error creating user"}
            ))
        return ServiceResult(user)


class UserCRUD(AppCRUD):
    def create_user(self, user_create: UserCreate) -> User:
        user = User(**user_create.dict())
        self.db.add(user)
        try:
            self.db.commit()
            self.db.refresh(user)
        except sqlalchemy.exc.DatabaseError as error:
            logger.error(f"{error}")
            user = None
        return user


