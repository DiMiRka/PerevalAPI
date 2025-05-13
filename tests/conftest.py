import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.main import app
from src.db import db_dependency
from src.models import PassPoint, User, Coords, Images


@pytest.fixture
def mock_db_session():
    session = AsyncMock(spec=AsyncSession)
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    yield session


@pytest.fixture
def client(mock_db_session):
    async def override_db_dependency():
        yield mock_db_session

    app.dependency_overrides[db_dependency] = override_db_dependency

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def mock_pass_point():
    mock = MagicMock(spec=PassPoint)
    mock.id = 1
    mock.status = "new"
    mock.beauty_title = "Test Pass"
    mock.title = "Test Title"
    mock.user = MagicMock(spec=User)
    mock.coords = MagicMock(spec=Coords)
    mock.images = [MagicMock(spec=Images)]
    return mock
