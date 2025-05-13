import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.main import app
from src.models import PassPoint, Coords, Images, User


@pytest.fixture()
def mock_db_session():
    session = AsyncMock(spec=AsyncSession)

    # Настройка моков для базовых методов
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    session.add = MagicMock()
    session.add_all = MagicMock()
    session.flush = AsyncMock()
    session.refresh = AsyncMock()

    yield session


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client
