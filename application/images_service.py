# images_service.py
import logging
import io
import zipfile
from typing import List, Optional
from fastapi import Depends
from domain.repositories.images_repository import ImagesRepository
from infrastructure.repositories.images_repository_impl import ImagesRepositoryImpl

logger = logging.getLogger(__name__)

class ImagesService:
    def __init__(self, images_repository: ImagesRepository = Depends(ImagesRepositoryImpl)) -> None:
        self.images_repository = images_repository

    def process_fields(self) -> bool:
        fields = self.images_repository.process_fields()
        if fields:
            images = self.images_repository.get_images_from_nasa_api(fields)
            upload_status = self.images_repository.upload_to_s3(images)
            logger.info("Images processed and uploaded to S3")
            return upload_status
        else:
            logger.warning("No fields processed")
            return False

    def list_images(self) -> Optional[List[str]]:
        return self.images_repository.list_images_in_s3()

    def download_images_as_zip(self) -> Optional[io.BytesIO]:
        images = self.images_repository.list_images_in_s3()
        if not images:
            logger.warning("No images available for download")
            return None
        return self._create_zip_from_images(image_keys=images)

    def download_images_by_field_id_as_zip(self, field_id: str) -> Optional[io.BytesIO]:
        images = self.images_repository.get_images_by_field_id(field_id)
        if not images:
            logger.warning(f"No images available for field ID {field_id}")
            return None
        return self._create_zip_from_images(image_keys=images)

    def _create_zip_from_images(self, image_keys: List[str]) -> io.BytesIO:
        images = self.images_repository.download_images_from_s3(image_keys)
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            for image in images:
                zip_file.writestr(image['key'], image['content'])
        zip_buffer.seek(0)
        logger.info("Created zip file from images")
        return zip_buffer
