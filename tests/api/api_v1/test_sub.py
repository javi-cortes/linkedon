from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings


def test_create_sub(client: TestClient, db: Session):
    data = {
        "email": "real@email.com",
        "salary_max": 60000,
        "salary_min": 30000,
    }
    response = client.post(
        f"{settings.API_V1_STR}/jobs/subscribe",
        json=data,
    )
    assert response.status_code == 200


def test_create_sub_wrong_email(client: TestClient, db: Session):
    data = {
        "email": "realemail.com",
        "salary_max": 60000,
        "salary_min": 30000,
    }
    response = client.post(
        f"{settings.API_V1_STR}/jobs/subscribe",
        json=data,
    )
    assert response.status_code == 422


def test_create_sub_empty_payload(client: TestClient, db: Session):
    response = client.post(
        f"{settings.API_V1_STR}/jobs/subscribe",
        json={},
    )
    assert response.status_code == 400

