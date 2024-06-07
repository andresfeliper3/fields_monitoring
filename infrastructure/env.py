import os
from dotenv import load_dotenv

load_dotenv()

NASA_API_KEY = os.environ.get('NASA_API_KEY')
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
LOCALSTACK_HOST = os.environ.get('LOCALSTACK_HOST')
LOCALSTACK_S3_PORT = os.environ.get('LOCALSTACK_S3_PORT')

env = {
    'NASA_API_KEY': NASA_API_KEY,
    'S3_BUCKET_NAME': S3_BUCKET_NAME,
    'LOCALSTACK_HOST': LOCALSTACK_HOST,
    'LOCALSTACK_S3_PORT': LOCALSTACK_S3_PORT
}