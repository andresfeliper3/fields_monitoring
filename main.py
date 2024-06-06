from fastapi import FastAPI, HTTPException, Response

from domain.nasa_imagery import process_fields, print_s3_buckets

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/image")
def read_image():
    content = process_fields()
    #media_type = response.headers.get("Content-Type", "image/png")
    return Response(content=content, media_type="image/png")
    #else:
     #   raise HTTPException(status_code=response.status_code, detail="Failed to fetch image")


@app.get("/s3")
def read_s3():
    print_s3_buckets()