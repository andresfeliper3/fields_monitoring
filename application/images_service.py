from infrastructure.repositories.nasa_images_repository import ImagesRepositoryImpl

class ImagesService:
    def __init__(self):
        self.images_repository = ImagesRepositoryImpl()

    def process_fields(self):
        fields = self.images_repository.process_fields()
        images = self.images_repository.get_images_from_nasa_api(fields)
        result = self.images_repository.upload_to_s3(images)
        return result

    def list_images(self):
        return self.images_repository.list_images_in_s3()
