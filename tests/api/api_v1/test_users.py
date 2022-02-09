from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.services.user import UserCRUD


def test_create_user(client: TestClient, user_crud: UserCRUD, db: Session):
    data = {
        'full_name': "full_name",
        'email': "fake@email.com",
    }
    response = client.post(
        f"{settings.API_V1_STR}/users",
        json=data,
    )
    assert response.status_code == 200


def test_create_user_without_email(client: TestClient, user_crud: UserCRUD, db: Session):
    data = {
        'full_name': "full_name"
    }
    response = client.post(
        f"{settings.API_V1_STR}/users",
        json=data,
    )
    assert response.status_code == 400


def test_create_user_invalid_email(client: TestClient, user_crud: UserCRUD, db: Session):
    data = {
        'full_name': "full_name",
        'email': "fakenotvalid@",
    }
    response = client.post(
        f"{settings.API_V1_STR}/users",
        json=data,
    )
    assert response.status_code == 422

