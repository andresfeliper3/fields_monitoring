import os
from dotenv import load_dotenv

load_dotenv()


env = {
    'NASA_API_KEY': os.environ.get('NASA_API_KEY'),
    'S3_BUCKET_NAME': os.environ.get('S3_BUCKET_NAME'),
    'LOCALSTACK_HOST': os.environ.get('LOCALSTACK_HOST'),
    'LOCALSTACK_S3_PORT': os.environ.get('LOCALSTACK_S3_PORT'),
    'SPECIFIED_DATE': os.environ.get('SPECIFIED_DATE'),
    'CSV_FILEPATH': os.environ.get('CSV_FILEPATH'),
    'ENDPOINT_URL': os.environ.get('ENDPOINT_URL')
}