from fastapi import HTTPException, status

class ImageNotFoundError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ImageProcessingError(Exception):
    """Exception raised for errors during image processing."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ImageFetchingError(Exception):
    """Exception raised for errors during image fetching."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ImageLoadingError(Exception):
    """Exception raised for errors during image loading."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class NoImagesAvailableError(HTTPException):
    """Exception raised when no images are available."""

    def __init__(self, detail="No images available"):
        self.detail = detail
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=self.detail)


class FieldProcessingError(Exception):
    """Exception raised for errors during field processing."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ImageDownloadingError(Exception):
    """Exception raised for errors during image downloading."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ImageUploadingError(Exception):
    """Exception raised for errors during image uploading."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ImageListingError(Exception):
    """Exception raised for errors during image listing."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)