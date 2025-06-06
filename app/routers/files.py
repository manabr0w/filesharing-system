from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
from app.__init__ import s3_service

router = APIRouter()

UPLOAD_DIR = "uploaded_files/"
DOWNLOAD_DIR = "downloaded_files/"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)

        result = s3_service.upload_file(file_location, s3_key=file.filename)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{filename}")
async def download_file(filename: str):
    try:
        destination_path = os.path.join(DOWNLOAD_DIR, filename)
        result = s3_service.download_file(s3_key=filename, destination_path=destination_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
