import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.main import app
from src.core import db_dependency
from src.models import PassPoint, User, Coords, Images


@pytest.fixture
def mock_db_session():
    session = AsyncMock(spec=AsyncSession)

    mock_pass = PassPoint(
        id=1,
        beauty_title="Test Pass",
        title="Test Title",
        other_titles="Test Other",
        status="new",
        user=User(email="test@example.com", phone="+123456789"),
        coords=Coords(latitude=12.345, longitude=54.321, height=1200),
        images=[Images(data="test", title="Test Image")]
    )

    async def execute_mock(query, *args, **kwargs):
        if "SELECT" in str(query):
            result = MagicMock()
            result.scalars.return_value.first.return_value = mock_pass
            return result
        return MagicMock()

    session.execute.side_effect = execute_mock
    session.commit.return_value = None
    session.refresh.return_value = None

    return session


@pytest.fixture
def client(mock_db_session):
    async def override_db_dependency():
        yield mock_db_session

    app.dependency_overrides = {db_dependency: override_db_dependency}

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
