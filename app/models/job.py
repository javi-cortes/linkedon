from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, \
    ARRAY
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Job(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)
    country = Column(String, nullable=False)
    posted_on = Column(DateTime(timezone=True), server_default=func.now())
    required_skills = Column(ARRAY(String))

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="jobs")
