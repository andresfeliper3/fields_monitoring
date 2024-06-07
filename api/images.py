from fastapi import APIRouter, HTTPException, Response, Depends
from application.images_service import ImagesService

router = APIRouter()

@router.get("/image")
def read_image(images_service: ImagesService = Depends()):
    content = images_service.process_fields()
    if content:
        return Response(content=content, media_type="image/png")
    else:
        raise HTTPException(status_code=404, detail="Failed to fetch image")
