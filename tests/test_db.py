import pytest
from unittest.mock import MagicMock, patch
from src.schemas import PassCreate, UserBase, LevelSchema, CoordsSchema, ImageSchema, PassUpdate
from src.models import PassPoint, StatusEnum
from src.services import db_post_pass, db_get_pass, db_patch_pass, db_get_passes_email
from datetime import datetime


@pytest.mark.asyncio
async def test_db_post_pass(mock_db_session):
    # Подготовка тестовых данных
    test_data = PassCreate(
        beauty_title="Test Pass",
        title="Test Title",
        other_titles="Test",
        conntent='',
        add_time=datetime.now(),
        user=UserBase(
            email="new@example.com",
            phone="+123456789",
            fam="Иванов",
            name="Иван",
            otc="Иванович"
        ),
        coords=CoordsSchema(latitude=45.234, longitude=3.123, height=1000),
        level=LevelSchema(winter="1A", summer="1B"),
        images=[ImageSchema(data="img1", title="Image 1")]
    )

    # Настройка моков
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db_session.execute.return_value = mock_result

    # Мок для возвращаемого значения
    mock_pass = MagicMock(spec=PassPoint)
    mock_pass.beauty_title = "Test Pass"
    mock_pass.status = StatusEnum.NEW

    with patch('src.models.PassPoint', return_value=mock_pass):
        result = await db_post_pass(mock_db_session, test_data)

    # Проверки
    assert result.beauty_title == "Test Pass"
    assert result.status == StatusEnum.NEW
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_db_get_pass(mock_db_session):
    # Создаём мок перевала
    mock_pass = MagicMock(spec=PassPoint)
    mock_pass.id = 1
    mock_pass.beauty_title = "Test Pass"

    # Настройка моков
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = mock_pass
    mock_db_session.execute.return_value = mock_result

    result = await db_get_pass(mock_db_session, 1)

    assert result.id == 1
    assert result.beauty_title == "Test Pass"


@pytest.mark.asyncio
async def test_db_patch(mock_db_session):
    # Мок существующего перевала
    mock_pass = MagicMock(spec=PassPoint)
    mock_pass.id = 1
    mock_pass.coords_id = 1

    # Тестовые данные для обновления
    update_data = PassUpdate(
        beauty_title="Updated Title",
        title="New Title",
        other_titles="Updated Other",
        connect="",
        add_time=datetime.now(),
        coords=CoordsSchema(latitude=46.234, longitude=9.789, height=1100),
        level=LevelSchema(winter="1A", summer="1B"),
        images=[ImageSchema(data="img1", title="Image 1")]
    )

    result = await db_patch_pass(mock_db_session, mock_pass, update_data)

    assert result["state"] == 1
    assert result["message"] == "Успешно обновлен"
    mock_db_session.execute.assert_awaited()
    mock_db_session.commit.assert_awaited_once()
