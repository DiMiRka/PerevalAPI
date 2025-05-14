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
    mock_db_session.execute.return_value.scalars.return_value.first.return_value = MagicMock(
        id=1, status="new", beauty_title="Test Pass"
    )

    response = client.get("/pass/pass_get/?pass_id=1")

    print(response.json())
    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.asyncio
async def test_get_pass_not_found(client, mock_db_session):
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db_session.execute.return_value = mock_result

    response = client.get("/pass/pass_get/?pass_id=999")

    print(response.json())
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_patch_pass_success(client, mock_db_session, mock_pass_point):
    test_data = get_test_data()
    test_data["user"]: {"additionalProp1": {}}

    response = client.patch("/pass/pass_patch/?pass_id=1", json=test_data)
    print(response)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_patch_pass_not_new_status(client, mock_db_session):
    mock_pass = MagicMock()
    mock_pass.status = "accepted"

    mock_db_session.execute.return_value = MagicMock(
        scalars=MagicMock(return_value=MagicMock(first=MagicMock(return_value=mock_pass)))
    )

    response = client.patch("/pass/pass_patch/?pass_id=1", json={"title": "New Title"})

    print(response.json())
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_passes_by_email_success(client, mock_db_session, mock_pass_point):
    mock_db_session.execute.return_value.scalars.return_value.all.return_value = [
        MagicMock(id=1, status="new")
    ]

    response = client.get("/pass/pass_get_email?email=test%40example.com")

    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_passes_by_email_not_found(client, mock_db_session):
    mock_db_session.execute.return_value = MagicMock(
        scalars=MagicMock(return_value=MagicMock(all=MagicMock(return_value=[])))
    )

    response = client.get("/pass/pass_get_email?email=notfound@example.com")

    print(response.json())
    assert response.status_code == 404
