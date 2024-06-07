import os
import csv
import requests
import boto3

from infrastructure.env import env

def download_image(lon, lat, date, dim):
    url = f"https://api.nasa.gov/planetary/earth/imagery/?lon={lon}&lat={lat}&date={date}&dim={dim}" \
          f"&api_key={env['NASA_API_KEY']}"
    print(url)
    response = requests.get(url)
    print("Status", response.status_code)
    return response.content if response.status_code == 200 else None

def upload_to_s3(image_content, field_id, date):
    folder_path = f"{field_id}/{date}_imagery.png"
    s3_client = boto3.client(
        "s3",
        endpoint_url=f"{env['LOCALSTACK_HOST']}:{env['LOCALSTACK_S3_PORT']}",
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy",
        region_name="us-east-1"
    )
    try:
        s3_client.put_object(Bucket=env['S3_BUCKET_NAME'], Key=folder_path, Body=image_content)
        print(f"Uploaded {folder_path} to {env['S3_BUCKET_NAME']}")
    except Exception as e:
        print(f"Failed to upload {folder_path}: {e}")

def process_fields():
    csv_file = 'domain/fields.csv'

    if not os.path.exists(csv_file):
        print(f"Error: '{csv_file}' not found in the current directory.")
        return

    results = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  #skip header
        for row in reader:
            field_id, lon, lat, dim = row
            date = '2018-01-01'
            image_content = download_image(lon, lat, date, dim)
            results.append(image_content)
            #if image_content is not None:
            print("Before upload")
            upload_to_s3(image_content, field_id, date)
            print("After upload")
    return results[0]

def print_s3_buckets():
    s3_client = boto3.client(
        "s3",
        endpoint_url=f"{env['LOCALSTACK_HOST']}:{env['LOCALSTACK_S3_PORT']}",
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy",
    )
    s3_client.create_bucket(Bucket=env['S3_BUCKET_NAME'])
    # List buckets to verify the bucket is created
    response = s3_client.list_buckets()
    print("List of buckets:")
    for bucket in response["Buckets"]:
        print(f'- {bucket["Name"]}')
    list_s3_objects()


def list_s3_objects():
    s3_client = boto3.client(
        "s3",
        endpoint_url=f"{env['LOCALSTACK_HOST']}:{env['LOCALSTACK_S3_PORT']}",
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy",
    )
    response = s3_client.list_objects_v2(Bucket=env['S3_BUCKET_NAME'])
    if 'Contents' in response:
        print("Objects in S3 bucket:")
        for obj in response['Contents']:
            print(f'- {obj["Key"]}')
    else:
        print("No objects found in S3 bucket.")