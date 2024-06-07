from fastapi import Depends
import io
import zipfile
from domain.repositories.images_repository import ImagesRepository
from infrastructure.repositories.nasa_images_repository import ImagesRepositoryImpl


class ImagesService:
    def __init__(self, images_repository: ImagesRepository = Depends(ImagesRepositoryImpl)):
        self.images_repository = images_repository

    def process_fields(self):
        fields = self.images_repository.process_fields()
        images = self.images_repository.get_images_from_nasa_api(fields)
        upload_status = self.images_repository.upload_to_s3(images)
        return upload_status

    def list_images(self):
        return self.images_repository.list_images_in_s3()

    def download_images_as_zip(self):
        images = self.images_repository.list_images_in_s3()
        if not images:
            return None
        return self._create_zip_from_images(image_keys=images)

    def download_images_by_field_id_as_zip(self, field_id):
        images = self.images_repository.get_images_by_field_id(field_id)
        if not images:
            return None
        return self._create_zip_from_images(image_keys=images)

    def _create_zip_from_images(self, image_keys):
        images = self.images_repository.download_images_from_s3(image_keys)
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            for image in images:
                zip_file.writestr(image['key'], image['content'])
        zip_buffer.seek(0)
        return zip_buffer