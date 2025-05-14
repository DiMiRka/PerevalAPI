import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from src.main import app
from src.db import db_dependency
from src.models import PassPoint, User, Coords, Images


@pytest.fixture
def mock_db_session():
    session = AsyncMock(spec=AsyncSession)

    # Настройка для успешных запросов
    success_mock = MagicMock()
    success_mock.scalars.return_value.first.return_value = MagicMock(id=1)
    success_mock.scalars.return_value.all.return_value = [MagicMock(id=1)]

    # Настройка для пустых результатов
    empty_mock = MagicMock()
    empty_mock.scalars.return_value.first.return_value = None
    empty_mock.scalars.return_value.all.return_value = []

    # По умолчанию возвращаем успешный результат
    session.execute.return_value = success_mock
    yield session


@pytest.fixture
def client(mock_db_session):
    async def override_db_dependency():
        yield mock_db_session

    original_overrides = app.dependency_overrides.copy()
    app.dependency_overrides[db_dependency] = override_db_dependency

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    app.dependency_overrides.update(original_overrides)


@pytest.fixture
def mock_pass_point():
    mock = MagicMock(spec=PassPoint)
    mock.id = 1
    mock.status = "new"
    mock.beauty_title = "Test Pass"
    mock.title = "Test Title"
    mock.other_titles = "Test Other"
    mock.connect = ""
    mock.add_time = datetime.now()

    mock.user = MagicMock(spec=User)
    mock.user.id = 1
    mock.user.email = "test@example.com"
    mock.user.fam = "Иванов"
    mock.user.name = "Иван"
    mock.user.otc = "Иванович"
    mock.user.phone = "+7-914-541-23-19"

    mock.coords = MagicMock(spec=Coords)
    mock.coords.latitude = 12.343
    mock.coords.longitude = 6.786
    mock.coords.height = 1000

    mock.images = [MagicMock(spec=Images)]
    mock.images[0].id = 1
    mock.images[0].data = "test_test_test_test"
    mock.images[0].title = "Test Image"

    return mock


@pytest.fixture
def mock_email ():
    mock = MagicMock()
    mock.send = AsyncMock(return_value=True)
    return mock
