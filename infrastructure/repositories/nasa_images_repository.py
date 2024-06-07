import os
import csv
import requests
import boto3
import botocore
import time
from infrastructure.env import env
from domain.repositories.images_repository import ImagesRepository
from domain.entities.field import Field

class ImagesRepositoryImpl(ImagesRepository):
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=f"{env['LOCALSTACK_HOST']}:{env['LOCALSTACK_S3_PORT']}",
            aws_access_key_id="dummy",
            aws_secret_access_key="dummy",
            region_name="us-east-1"
        )
        self.bucket_name = env['S3_BUCKET_NAME']
        self.s3_client.create_bucket(Bucket=self.bucket_name)
        time.sleep(5)


    def download_image(self, lon, lat, date, dim):
        url = f"https://api.nasa.gov/planetary/earth/imagery/?lon={lon}&lat={lat}&date={date}&dim={dim}&api_key={env['NASA_API_KEY']}"
        response = requests.get(url)
        return response.content if response.status_code == 200 else None

    def upload_to_s3(self, images):
        for image in images:
            folder_path = f"{image['field'].field_id}/{image['field '].date}_imagery.png"
            try:
                self.s3_client.put_object(Bucket=self.bucket_name, Key=folder_path, Body=image['image_content'])
                print(f"Uploaded {folder_path} to {self.bucket_name}")
            except Exception as e:
               raise Exception(f"There was an error uploading the images to S3: {e}")
        return True

    def process_fields(self):
        csv_file = 'domain/fields.csv'

        if not os.path.exists(csv_file):
            print(f"Error: '{csv_file}' not found.")
            return

        fields = []
        date = '2018-01-01'
        with open(csv_file, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader)  # skip header
            for row in reader:
                field_id, lon, lat, dim = row
                field = Field(field_id=field_id, lon=float(lon), lat=float(lat), dim=float(dim), date=date)
                fields.append(field)

        return fields

    def get_images_from_nasa_api(self, fields):
        images = []
        for field in fields:
            try:
                image_content = self.download_image(field.lon, field.lat, field.date, field.dim)
                images.append({'image_content': image_content, 'field': field})
            except Exception as e:
                raise Exception(f"There was an error downloading the image from NASA API: {e}")
        return images

    def list_images_in_s3(self):
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            images = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    images.append(obj['Key'])
            return images
        except Exception as e:
            raise Exception(f"There was an error listing the images in S3: {e}")