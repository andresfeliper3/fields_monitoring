import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from application.images_service import ImagesService
from domain.repositories.images_repository import ImagesRepository
from typing import List, Optional
import io

@pytest.fixture
def images_repository_mock():
    mock = MagicMock(spec=ImagesRepository)
    return mock

@pytest.fixture
def images_service(images_repository_mock):
    return ImagesService(images_repository=images_repository_mock)

def test_load_images_from_nasa_api(images_service, images_repository_mock):
    images_repository_mock.process_fields.return_value = [{'id': 'field1'}, {'id': 'field2'}]
    images_repository_mock.get_images_from_nasa_api.return_value = [{'image': 'image1'}, {'image': 'image2'}]
    images_repository_mock.upload_to_s3.return_value = True

    result = images_service.load_images_from_nasa_api()

    assert result == True
    images_repository_mock.process_fields.assert_called_once()
    images_repository_mock.get_images_from_nasa_api.assert_called_once()
    images_repository_mock.upload_to_s3.assert_called_once()

def test_list_images(images_service, images_repository_mock):
    images_repository_mock.list_images_in_s3.return_value = ["image1.jpg", "image2.jpg"]

    result = images_service.list_images()

    assert result == ["image1.jpg", "image2.jpg"]
    images_repository_mock.list_images_in_s3.assert_called_once()

def test_download_images_as_zip(images_service, images_repository_mock):
    images_repository_mock.list_images_in_s3.return_value = ["image1.jpg", "image2.jpg"]
    images_repository_mock.download_images_from_s3.return_value = [
        {'key': 'image1.jpg', 'content': b'content1'},
        {'key': 'image2.jpg', 'content': b'content2'}
    ]

    zip_buffer = images_service.download_images_as_zip()

    assert zip_buffer is not None
    assert isinstance(zip_buffer, io.BytesIO)
    images_repository_mock.list_images_in_s3.assert_called_once()
    images_repository_mock.download_images_from_s3.assert_called_once()

def test_download_images_by_field_id_as_zip(images_service, images_repository_mock):
    field_id = "12345"
    images_repository_mock.get_images_by_field_id.return_value = ["image1.jpg", "image2.jpg"]
    images_repository_mock.download_images_from_s3.return_value = [
        {'key': 'image1.jpg', 'content': b'content1'},
        {'key': 'image2.jpg', 'content': b'content2'}
    ]

    zip_buffer = images_service.download_images_by_field_id_as_zip(field_id)

    assert zip_buffer is not None
    assert isinstance(zip_buffer, io.BytesIO)
    images_repository_mock.get_images_by_field_id.assert_called_once_with(field_id)
    images_repository_mock.download_images_from_s3.assert_called_once()

def test_process_fields_from_file(images_service, images_repository_mock):
    images_repository_mock.process_fields.return_value = [{'id': 'field1'}, {'id': 'field2'}]

    fields = images_service._process_fields_from_file()

    assert fields == [{'id': 'field1'}, {'id': 'field2'}]
    images_repository_mock.process_fields.assert_called_once()

def test_fetch_images_from_nasa_api(images_service, images_repository_mock):
    images_repository_mock.process_fields.return_value = [{'id': 'field1'}, {'id': 'field2'}]
    images_repository_mock.get_images_from_nasa_api.return_value = [{'image': 'image1'}, {'image': 'image2'}]

    images = images_service._fetch_images_from_nasa_api()

    assert images == [{'image': 'image1'}, {'image': 'image2'}]
    images_repository_mock.process_fields.assert_called_once()
    images_repository_mock.get_images_from_nasa_api.assert_called_once()

def test_create_zip_from_images(images_service, images_repository_mock):
    image_keys = ["image1.jpg", "image2.jpg"]
    images_repository_mock.download_images_from_s3.return_value = [
        {'key': 'image1.jpg', 'content': b'content1'},
        {'key': 'image2.jpg', 'content': b'content2'}
    ]

    zip_buffer = images_service._create_zip_from_images(image_keys)

    assert zip_buffer is not None
    assert isinstance(zip_buffer, io.BytesIO)
    images_repository_mock.download_images_from_s3.assert_called_once_with(image_keys)
