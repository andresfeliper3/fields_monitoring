import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from fastapi import status
from main import app

from application.images_service import ImagesService


@pytest.fixture
def images_service_mock():
    mock = MagicMock(spec=ImagesService)
    mock.load_images_from_nasa_api = AsyncMock(return_value=True)
    mock.list_images = AsyncMock(return_value=["image1.jpg", "image2.jpg"])
    mock.download_images_as_zip = AsyncMock(return_value=b'zipcontent')
    mock.download_images_by_field_id_as_zip = AsyncMock(return_value=b'zipcontent')
    return mock


@pytest.mark.asyncio
async def test_load_images(images_service_mock, monkeypatch):
    # Mock the dependency
    monkeypatch.setattr(ImagesService, "__call__", lambda: images_service_mock)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/load-images")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "success", "message": "Images processed and uploaded successfully"}


@pytest.mark.asyncio
async def test_list_images(images_service_mock, monkeypatch):
    monkeypatch.setattr(ImagesService, "__call__", lambda: images_service_mock)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/images")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "success"


@pytest.mark.asyncio
async def test_download_images_zip(images_service_mock, monkeypatch):
    monkeypatch.setattr(ImagesService, "__call__", lambda: images_service_mock)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/images/zip")

    assert response.status_code == status.HTTP_200_OK
    assert response.headers['Content-Disposition'] == 'attachment;filename=images.zip'


@pytest.mark.asyncio
async def test_download_images_by_field_id_zip(images_service_mock, monkeypatch):
    monkeypatch.setattr(ImagesService, "__call__", lambda: images_service_mock)

    field_id = "1"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(f"/images/zip/{field_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.headers['Content-Disposition'] == f'attachment;filename={field_id}_images.zip'
