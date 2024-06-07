# tests/test_infrastructure/test_images_repository_impl.py

import pytest
import requests
from unittest.mock import MagicMock, patch, mock_open
from infrastructure.repositories.images_repository_impl import ImagesRepositoryImpl
from domain.entities.field import Field
import boto3
from moto import mock_s3
import io

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("ENDPOINT_URL", "https://example.com")
    monkeypatch.setenv("NASA_API_KEY", "fake-api-key")
    monkeypatch.setenv("LOCALSTACK_HOST", "http://localhost")
    monkeypatch.setenv("LOCALSTACK_S3_PORT", "4566")
    monkeypatch.setenv("S3_BUCKET_NAME", "test-bucket")
    monkeypatch.setenv("CSV_FILEPATH", "fields.csv")
    monkeypatch.setenv("SPECIFIED_DATE", "2023-01-01")

@pytest.fixture
def s3_client(mock_env):
    with mock_s3():
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        yield s3

@pytest.fixture
def images_repository_impl(s3_client):
    return ImagesRepositoryImpl()

def test_process_fields(images_repository_impl, monkeypatch):
    mock_csv_content = "field_id;lon;lat;dim\nfield1;10.0;20.0;0.1\nfield2;30.0;40.0;0.2\n"
    monkeypatch.setattr("builtins.open", mock_open(read_data=mock_csv_content))

    fields = images_repository_impl.process_fields()

    assert len(fields) == 2
    assert fields[0].field_id == "field1"
    assert fields[1].field_id == "field2"

@patch("requests.get")
def test_get_images_from_nasa_api(mock_get, images_repository_impl):
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b"fake-image-content"

    fields = [Field(field_id="field1", lon=10.0, lat=20.0, dim=0.1, date="2023-01-01")]

    images = images_repository_impl.get_images_from_nasa_api(fields)

    assert len(images) == 1
    assert images[0]['image_content'] == b"fake-image-content"

@patch("requests.get")
def test_download_image(mock_get, images_repository_impl):
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b"fake-image-content"

    content = images_repository_impl.download_image(10.0, 20.0, "2023-01-01", 0.1)

    assert content == b"fake-image-content"

def test_upload_to_s3(images_repository_impl, s3_client):
    images = [
        {'image_content': b"fake-image-content", 'field': Field(field_id="field1", lon=10.0, lat=20.0, dim=0.1, date="2023-01-01")}
    ]

    result = images_repository_impl.upload_to_s3(images)

    assert result == True




