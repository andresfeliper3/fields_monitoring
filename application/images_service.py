import logging
import io
import zipfile
from fastapi import Depends
from typing import List, Optional
from domain.repositories.images_repository import ImagesRepository
from infrastructure.repositories.images_repository_impl import ImagesRepositoryImpl
from domain.entities.field import Field
from domain.custom_exceptions import ImageProcessingError, ImageFetchingError, ImageLoadingError, NoImagesAvailableError

logger = logging.getLogger(__name__)

class ImagesService:
    def __init__(self, images_repository: ImagesRepository = Depends(ImagesRepositoryImpl)) -> None:
        self.images_repository: ImagesRepository = images_repository

    def _process_fields_from_file(self) -> Optional[List[Field]]:
        try:
            fields: Optional[List[Field]] = self.images_repository.process_fields()
            return fields
        except Exception as e:
            raise ImageProcessingError(f"There was an error processing the fields: {e}")

    def _fetch_images_from_nasa_api(self) -> List[dict]:
        try:
            fields: Optional[List[Field]] = self._process_fields_from_file()
            images: List[dict] = self.images_repository.get_images_from_nasa_api(fields)
            logger.debug(images)
            return images
        except Exception as e:
            raise ImageFetchingError(f"There was an error fetching images from NASA API: {e}")

    def load_images_from_nasa_api(self) -> bool:
        try:
            images: List[dict] = self._fetch_images_from_nasa_api()
            upload_status: bool = self.images_repository.upload_to_s3(images)
            logger.info("Images processed and uploaded")
            return upload_status
        except Exception as e:
            raise ImageLoadingError(f"There was an error loading images: {e}")

    def list_images(self) -> Optional[List[str]]:
        try:
            return self.images_repository.list_images_in_s3()
        except Exception as e:
            raise ImageFetchingError(f"There was an error listing images in S3: {e}")

    def download_images_as_zip(self) -> Optional[io.BytesIO]:
        try:
            images: Optional[List[str]] = self.images_repository.list_images_in_s3()
            if not images:
                logger.warning("No images available for download")
                return None
            return self._create_zip_from_images(image_keys=images)
        except Exception as e:
            raise ImageFetchingError(f"There was an error downloading images from S3: {e}")

    def download_images_by_field_id_as_zip(self, field_id: str) -> Optional[io.BytesIO]:
        try:
            images: Optional[List[str]] = self.images_repository.get_images_by_field_id(field_id)
            if not images:
                logger.warning(f"No images available for field ID {field_id}")
                return None
            return self._create_zip_from_images(image_keys=images)
        except Exception as e:
            raise ImageFetchingError(f"There was an error downloading images for field ID {field_id} from S3: {e}")

    def _create_zip_from_images(self, image_keys: List[str]) -> io.BytesIO:
        try:
            images: List[dict] = self.images_repository.download_images_from_s3(image_keys)
            zip_buffer: io.BytesIO = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
                for image in images:
                    zip_file.writestr(image['key'], image['content'])
            zip_buffer.seek(0)
            logger.info("Created zip file from images")
            return zip_buffer
        except Exception as e:
            raise ImageProcessingError(f"There was an error creating zip file from images: {e}")
