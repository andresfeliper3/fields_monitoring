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
