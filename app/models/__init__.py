# make sure all SQL Alchemy models are imported (app.db.__init__) before
# initializing DB otherwise, SQL Alchemy might fail to initialize
# relationships properly for more details:
# https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

from .job import Job
from .user import User
from .email_sub import EmailSub
