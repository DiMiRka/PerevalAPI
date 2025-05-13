import pytest
from fastapi import status
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from src.models import PassPoint, User, Coords, StatusEnum


def get_test_data():
    return {
        "beauty_title": "Test Pass",
        "title": "Test Title",
        "other_titles": "Test Other",
        "connect": "",
        "add_time": datetime.now().isoformat(),
        "user": {
            "email": "test@example.com",
            "phone": "+123456789",
            "fam": "Иванов",
            "name": "Иван",
            "otc": "Иванович"
        },
        "coords": {
            "latitude": 5.345,
            "longitude": 9.468,
            "height": 1000
        },
        "level": {
            "winter": "",
            "summer": "",
            "autumn": "",
            "spring": "1A"
        },
        "images": [
            {"data": "img1", "title": "Image 1"}
        ]
    }


@pytest.mark.asyncio
async def test_post_pass_success(client, mock_db_session, mock_pass_point):
    mock_pass = MagicMock(spec=PassPoint)
    mock_pass.id = 1
    mock_db_session.execute.return_value = MagicMock(
        scalars=MagicMock(return_value=MagicMock(first=MagicMock(return_value=None))))

    response = client.post("/pass/pass_post", json=get_test_data())

    assert response.status_code == status.HTTP_200_OK
    print(response.json())
    assert response.json()["status"] == 200
    assert isinstance(response.json()["id"], int)


@pytest.mark.asyncio
async def test_post_pass_validation_error(client):
    invalid_data = get_test_data()
    invalid_data["user"]["email"] = "invalid-email"

    response = client.post("/pass/pass_post", json=invalid_data)

    print(response.json())
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_pass_success(client, mock_db_session, mock_pass_point):
    mock_pass = MagicMock()
    mock_pass.id = 1
    mock_pass.status = "new"
    mock_pass.beauty_title = "Test Pass"

    mock_result = MagicMock()
    mock_scalar_result = MagicMock()
    mock_scalar_result.first.return_value = mock_pass
    mock_result.scalars.return_value = mock_scalar_result
    mock_db_session.execute.return_value = mock_result

    response = client.get("/pass/pass_get/1")

    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["beauty_title"] == "Test Pass"


@pytest.mark.asyncio
async def test_get_pass_not_found(client, mock_db_session):
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db_session.execute.return_value = mock_result

    response = client.get("/pass/pass_get/999")

    print(response.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Pereval not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_patch_pass_success(client, mock_db_session, mock_pass_point):
    mock_db_session.execute.side_effect = [
        MagicMock(scalars=MagicMock(return_value=MagicMock(first=MagicMock(return_value=mock_pass_point)))), MagicMock()
    ]

    update_data = get_test_data()
    update_data["title"] = "Updated Title"

    response = client.patch("/pass/pass_patch/1", json=update_data)

    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["state"] == 1


@pytest.mark.asyncio
async def test_patch_pass_not_new_status(client, mock_db_session):
    mock_pass = MagicMock()
    mock_pass.id = 1
    mock_pass.status = StatusEnum.ACCEPTED

    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = mock_pass
    mock_db_session.execute.return_value = mock_result

    response = client.patch("/pass/pass_patch/1", json=get_test_data())

    print(response.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "The pass does not have the 'new'" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_passes_by_email_success(client, mock_db_session, mock_pass_point):
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_pass_point]
    mock_db_session.execute.return_value = mock_result

    response = client.get("/pass/pass_get_email?email=test@example.com")

    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Test Title"


@pytest.mark.asyncio
async def test_get_passes_by_email_not_found(client, mock_db_session):
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_db_session.execute.return_value = mock_result

    response = client.get("/pass/pass_get_email?email=notfound@example.com")

    print(response.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "No found for email" in response.json()["detail"]
