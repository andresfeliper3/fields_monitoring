from abc import ABC, abstractmethod

class ImagesRepository(ABC):
    @abstractmethod
    def download_image(self, lon, lat, date, dim):
        pass

    @abstractmethod
    def upload_to_s3(self, images):
        pass

    @abstractmethod
    def process_fields(self):
        pass

    @abstractmethod
    def get_images_from_nasa_api(self, fields):
        pass

    @abstractmethod
    def list_images_in_s3(self):
        pass

    @abstractmethod
    def get_images_by_field_id(self, field_id):
        pass

    @abstractmethod
    def download_images_from_s3(self, image_keys):
        pass

class ImagesRepositoryImpl(ImagesRepository):
    def __init__(self, s3_client, bucket_name):
        self.s3_client = s3_client
        self.bucket_name = bucket_name

    def download_image(self, lon, lat, date, dim):
        # Implementation for downloading image
        pass

    def upload_to_s3(self, images):
        # Implementation for uploading images to S3
        pass

    def process_fields(self):
        # Implementation for processing fields
        pass

    def get_images_from_nasa_api(self, fields):
        # Implementation for getting images from NASA API
        pass

    def list_images_in_s3(self):
        # Implementation for listing images in S3
        pass

    def get_images_by_field_id(self, field_id):
        # Implementation for getting images by field ID
        pass

    def download_images_from_s3(self, image_keys):
        # Implementation for downloading images from S3
        pass
