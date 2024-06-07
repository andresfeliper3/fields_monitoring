import os
import csv
import requests
import boto3
import botocore
import time
import logging
import httpx

from typing import List, Optional
from infrastructure.env import env
from infrastructure.utils.URLBuilder import NasaApiUrlBuilder
from domain.repositories.images_repository import ImagesRepository
from domain.entities.field import Field
from domain.custom_exceptions import FieldProcessingError, ImageFetchingError, ImageDownloadingError, ImageUploadingError, ImageListingError

logger = logging.getLogger(__name__)

class ImagesRepositoryImpl(ImagesRepository):
    def __init__(self) -> None:
        self.ENDPOINT_URL = env['ENDPOINT_URL']
        self.API_KEY = env['NASA_API_KEY']
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=f"{env['LOCALSTACK_HOST']}:{env['LOCALSTACK_S3_PORT']}",
            aws_access_key_id="dummy",
            aws_secret_access_key="dummy",
            region_name="us-east-1"
        )
        self.bucket_name: str = env['S3_BUCKET_NAME']
        self.s3_client.create_bucket(Bucket=self.bucket_name)
        self.s3_client.get_waiter('bucket_exists').wait(Bucket=self.bucket_name)
        logger.info("S3 client initialized and bucket created")

    def process_fields(self) -> Optional[List[Field]]:
        csv_file: str = env['CSV_FILEPATH']

        if not os.path.exists(csv_file):
            logger.error(f"Error: '{csv_file}' not found.")
            raise FieldProcessingError(f"Error: '{csv_file}' not found.")

        fields: List[Field] = []
        with open(csv_file, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader)  # skip header
            for row in reader:
                field_id, lon, lat, dim = row
                field = Field(field_id=field_id, lon=float(lon), lat=float(lat), dim=float(dim),
                              date=env['SPECIFIED_DATE'])
                fields.append(field)
                logger.info(f"Processed field {field_id} with coordinates ({lon}, {lat})")

        return fields

    def get_images_from_nasa_api(self, fields: List[Field]) -> List[dict]:
        images: List[dict] = []
        for field in fields:
            try:
                image_content: Optional[bytes] = self.download_image(field.lon, field.lat, field.date, field.dim)
                images.append({'image_content': image_content, 'field': field})
                logger.info(f"Image for field {field.field_id} downloaded from NASA API")
            except Exception as e:
                raise ImageFetchingError(f"There was an error fetching images from NASA API: {e}")
        return images

    def download_image(self, lon: float, lat: float, date: str, dim: float) -> Optional[bytes]:
        url = NasaApiUrlBuilder(self.ENDPOINT_URL) \
            .set_lon(lon) \
            .set_lat(lat) \
            .set_date(date) \
            .set_dim(dim) \
            .set_api_key(self.API_KEY) \
            .build()

        try:
            response = requests.get(url)
            response.raise_for_status()
            logger.info(f"Image downloaded for coordinates ({lon}, {lat}) on {date}")
            return response.content
        except requests.RequestException as e:
            logger.warning(f"Failed to download image for coordinates ({lon}, {lat}) on {date}: {e}")
            raise ImageDownloadingError(f"There was an error downloading the image from NASA API: {e}")

    def upload_to_s3(self, images: List[dict]) -> bool:
        try:
            for image in images:
                folder_path: str = f"{image['field'].field_id}/{image['field'].date}_imagery.png"
                self.s3_client.put_object(Bucket=self.bucket_name, Key=folder_path, Body=image['image_content'])
                logger.info(f"Uploaded {folder_path} to {self.bucket_name}")
            return True
        except Exception as e:
            logger.error(f"There was an error uploading the images to S3: {e}")
            raise ImageUploadingError(f"There was an error uploading the images to S3: {e}")

    def list_images_in_s3(self) -> Optional[List[str]]:
        try:
            response: dict = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            images: List[str] = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    images.append(obj['Key'])
            logger.info("Listed images in S3")
            return images
        except Exception as e:
            logger.error(f"There was an error listing the images in S3: {e}")
            raise ImageListingError(f"There was an error listing the images in S3: {e}")

    def get_images_by_field_id(self, field_id: str) -> Optional[List[str]]:
        try:
            response: dict = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=f"{field_id}/")
            images: List[str] = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    images.append(obj['Key'])
            logger.info(f"Listed images for field ID {field_id} in S3")
            return images
        except Exception as e:
            logger.error(f"There was an error listing the images for field ID {field_id} in S3: {e}")
            raise ImageListingError(f"There was an error listing the images for field ID {field_id} in S3: {e}")

    def download_images_from_s3(self, image_keys: List[str]) -> List[dict]:
        images: List[dict] = []
        for image_key in image_keys:
            try:
                response: dict = self.s3_client.get_object(Bucket=self.bucket_name, Key=image_key)
                images.append({'key': image_key, 'content': response['Body'].read()})
                logger.info(f"Downloaded image {image_key} from S3")
            except Exception as e:
                logger.error(f"There was an error downloading the image {image_key} from S3: {e}")
                raise ImageDownloadingError(f"There was an error downloading the image {image_key} from S3: {e}")
        return images

