from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import StreamingResponse
from application.images_service import ImagesService

router = APIRouter()

@router.get("/load-images")
def load_images(images_service: ImagesService = Depends(ImagesService)):
    result = images_service.load_images_from_nasa_api()
    if result:
        return {"status": "success", "message": "Images processed and uploaded successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to fetch images")

@router.get("/images")
def list_images(images_service: ImagesService = Depends(ImagesService)):
    images = images_service.list_images()
    if images:
        return {"status": "success", "images": images}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="No images found in S3 bucket")

@router.get("/images/zip")
def download_images_zip(images_service: ImagesService = Depends(ImagesService)):
    zip_buffer = images_service.download_images_as_zip()
    if zip_buffer:
        return StreamingResponse(
            zip_buffer,
            media_type='application/x-zip-compressed',
            headers={'Content-Disposition': 'attachment;filename=images.zip'}
        )
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No images found")

@router.get("/images/zip/{field_id}")
def download_images_by_field_id_zip(field_id: str, images_service: ImagesService = Depends(ImagesService)):
    zip_buffer = images_service.download_images_by_field_id_as_zip(field_id)
    if zip_buffer:
        return StreamingResponse(
            zip_buffer,
            media_type='application/x-zip-compressed',
            headers={'Content-Disposition': f'attachment;filename={field_id}_images.zip'}
        )
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No images found for field ID {field_id}")
