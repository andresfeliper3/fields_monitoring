from fastapi import APIRouter, HTTPException, Response, Depends
from application.images_service import ImagesService

router = APIRouter()

@router.get("/load-images")
def load_images(images_service: ImagesService = Depends()):
    result = images_service.process_fields()
    if result:
        return {"status": "success", "message": "Images processed and uploaded successfully"}
    else:
        raise HTTPException(status_code=404, detail="Failed to fetch images")


@router.get("/images")
def list_images(images_service: ImagesService = Depends(ImagesService)):
    images = images_service.list_images()
    if images:
        return {"status": "success", "images": images}
    else:
        raise HTTPException(status_code=404, detail="No images found in S3 bucket")
