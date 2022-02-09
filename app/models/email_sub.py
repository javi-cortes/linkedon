from sqlalchemy import Column, Integer
from sqlalchemy_utils import EmailType

from app.db.base_class import Base


class EmailSub(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(EmailType, nullable=False)
    # search patterns
    salary_max = Column(Integer, nullable=True)
    salary_min = Column(Integer, nullable=True)
