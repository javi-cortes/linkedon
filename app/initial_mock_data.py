import random
import sys

from app.api.deps import get_db
from app.schemas.job import JobCreate
from app.services.job import JobService


def jobs_randomize(jobs_amount):
    return [
        JobCreate(
            name=random.choice(NAMES),
            description=random.choice(DESCRIPTIONS),
            user_id=random.choice([4, 5, 6]),  # change this
            salary=random.choice(SALARIES),
            required_skills=random.sample(SKILLS, 3),
            country=random.choice(COUNTRIES),
        )
        for __ in range(jobs_amount)
    ]


def create_dummy_jobs(jobs_amount):
    job_service = JobService(next(get_db()))
    for dummy_job in jobs_randomize(jobs_amount):
        job_service.create_job(dummy_job)


NAMES = (
    "Jr Java Developer",
    "SSr Java Developer",
    "Sr Java Developer",
    "Jr PHP Developer",
    "SSr PHP Developer",
    "Sr Developer",
    "Functional Analyst",
    "Jr Python Developer",
    "React Developer",
    "Angular Developer",
    "Database Analyst",
    "Database Administrator",
    "Linux Admin",
    "Windows server Admin",
    "Jr UX Designer",
    "Sr UX Designer",
    "Go Developer",
    "Jr C# Developer"
    "SSr C# Developer"
    "Sr C# Developer"
    "Sr C++ Developer"
    "Sr C Developer",
    "Ruby Developer",
)

DESCRIPTIONS = (
    """
    Integrated within a collaborative development's team, you will help us deliver our product
    """,
    """
    Work on high data volumes and extract data intelligence for easy access, with low latency. 
    Use data to measure performance and improved targeting (data augmentors)
    Provide back-end features for our SaaS product (user management, payments, application metrology)
    Deliver in a fast-paced environment using edge infrastructure 
    (CI/CD, Cloud-native technologies around Kubernetes, GitOps workflow, AWS environment). 
    """,
    """
    We like to empower developers to be autonomous from development to production
    Take active part to continuously improve our code quality, metrology, alerting
    Depending on your experience, mentor junior back-end engineer(s)
    """,
)

SALARIES = (
    25000,
    35000,
    45000,
    55000,
    65000,
    75000,
    85000,
    95000,
)

COUNTRIES = (
    "Spain",
    "UK",
    "EEUU",
    "Germany",
)

SKILLS = (
    "Java",
    "OOP",
    "Design Patterns",
    "PHP",
    "UX",
    "Python",
    "React",
    "TypeScript",
    "Angular",
    "MySQL",
    "Percona",
    "Linux",
    "Docker",
    "Windows Server",
    "Go",
    "C#",
    "C++",
    "C",
    "Ruby",
    "BI",
    "Networking",
    "IT",
    "Kotlin",
    "OOP",
)

if __name__ == "__main__":
    create_dummy_jobs(30)
