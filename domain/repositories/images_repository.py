from abc import ABC, abstractmethod

class ImagesRepository(ABC):
    @abstractmethod
    def process_fields(self):
        pass
