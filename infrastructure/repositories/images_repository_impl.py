import os
import csv
import requests
import boto3
import botocore
import time
from typing import List, Optional, Any, Union
from infrastructure.env import env
from domain.repositories.images_repository import ImagesRepository
from domain.entities.field import Field


class ImagesRepositoryImpl(ImagesRepository):
    def __init__(self) -> None:
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=f"{env['LOCALSTACK_HOST']}:{env['LOCALSTACK_S3_PORT']}",
            aws_access_key_id="dummy",
            aws_secret_access_key="dummy",
            region_name="us-east-1"
        )
        self.bucket_name: str = env['S3_BUCKET_NAME']
        self.s3_client.create_bucket(Bucket=self.bucket_name)
        time.sleep(5)

    def process_fields(self) -> Optional[List[Field]]:
        csv_file: str = 'domain/fields.csv'

        if not os.path.exists(csv_file):
            print(f"Error: '{csv_file}' not found.")
            return None

        fields: List[Field] = []
        date: str = '2018-01-01'
        with open(csv_file, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader)  # skip header
            for row in reader:
                field_id, lon, lat, dim = row
                field = Field(field_id=field_id, lon=float(lon), lat=float(lat), dim=float(dim), date=date)
                fields.append(field)

        return fields

    def get_images_from_nasa_api(self, fields: List[Field]) -> List[dict]:
        images: List[dict] = []
        for field in fields:
            try:
                image_content: Optional[bytes] = self.download_image(field.lon, field.lat, field.date, field.dim)
                images.append(
                    {
                        'image_content': image_content,
                        'field': field
                     }
                )
            except Exception as e:
                raise Exception(f"There was an error downloading the image from NASA API: {e}")
        return images

    def download_image(self, lon: float, lat: float, date: str, dim: float) -> Optional[bytes]:
        url = f"https://api.nasa.gov/planetary/earth/imagery/?lon={lon}&lat={lat}&date={date}&dim={dim}&api_key={env['NASA_API_KEY']}"
        response = requests.get(url)
        return response.content if response.status_code == 200 else None

    def upload_to_s3(self, images: List[dict]) -> bool:
        for image in images:
            folder_path: str = f"{image['field'].field_id}/{image['field'].date}_imagery.png"
            try:
                self.s3_client.put_object(Bucket=self.bucket_name, Key=folder_path, Body=image['image_content'])
                print(f"Uploaded {folder_path} to {self.bucket_name}")
            except Exception as e:
                raise Exception(f"There was an error uploading the images to S3: {e}")
        return True


    def list_images_in_s3(self) -> Optional[List[str]]:
        try:
            response: dict = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            images: List[str] = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    images.append(obj['Key'])
            return images
        except Exception as e:
            raise Exception(f"There was an error listing the images in S3: {e}")

    def get_images_by_field_id(self, field_id: str) -> Optional[List[str]]:
        try:
            response: dict = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=f"{field_id}/")
            images: List[str] = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    images.append(obj['Key'])
            return images
        except Exception as e:
            raise Exception(f"There was an error listing the images for field ID {field_id} in S3: {e}")

    def download_images_from_s3(self, image_keys: List[str]) -> List[dict]:
        images: List[dict] = []
        for image_key in image_keys:
            try:
                response: dict = self.s3_client.get_object(Bucket=self.bucket_name, Key=image_key)
                images.append({'key': image_key, 'content': response['Body'].read()})
            except Exception as e:
                raise Exception(f"There was an error downloading the image {image_key} from S3: {e}")
        return images
