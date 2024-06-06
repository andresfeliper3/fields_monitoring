import os
import csv
import requests
import boto3
import botocore
import time
from infrastructure.env import env
from domain.repositories.images_repository import ImagesRepository

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

    def upload_to_s3(self, image_content, field_id, date):
        folder_path = f"{field_id}/{date}_imagery.png"
        try:
            self.s3_client.put_object(Bucket=self.bucket_name, Key=folder_path, Body=image_content)
            print(f"Uploaded {folder_path} to {self.bucket_name}")
        except Exception as e:
            print(f"Failed to upload {folder_path}: {e}")

    def process_fields(self):
        csv_file = 'domain/fields.csv'

        self.print_s3_buckets()

        if not os.path.exists(csv_file):
            print(f"Error: '{csv_file}' not found.")
            return

        results = []
        with open(csv_file, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader)  # skip header
            for row in reader:
                field_id, lon, lat, dim = row
                date = '2018-01-01'
                image_content = self.download_image(lon, lat, date, dim)
                if image_content:
                    self.upload_to_s3(image_content, field_id, date)
                results.append(image_content)
        return results[0] if results else None


    def list_s3_objects(self):
        response = self.s3_client.list_objects_v2(Bucket=env['S3_BUCKET_NAME'])
        if 'Contents' in response:
            print("Objects in S3 bucket:")
            for obj in response['Contents']:
                print(f'- {obj["Key"]}')
        else:
            print("No objects found in S3 bucket.")


    def print_s3_buckets(self):
        response = self.s3_client.list_buckets()
        print("List of buckets:")
        for bucket in response["Buckets"]:
            print(f'- {bucket["Name"]}')