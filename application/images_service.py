from infrastructure.repositories.nasa_images_repository import ImagesRepositoryImpl

class ImagesService:
    def __init__(self):
        self.images_repository = ImagesRepositoryImpl()

    def process_fields(self):
        return self.images_repository.process_fields()
