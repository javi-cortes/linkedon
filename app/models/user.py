from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(EmailType, nullable=False)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    jobs = relationship("Job", back_populates="user")
