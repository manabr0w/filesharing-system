from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from app.services import s3_service

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        result = await s3_service.upload_uploadfile(file, s3_key=file.filename)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{filename}")
async def download_file(filename: str):
    try:
        downloads_path = os.path.expanduser(f"~/Downloads/{filename}")
        s3_service.download_file(s3_key=filename, destination_path=downloads_path)

        return {
            "message": f"File '{filename}' saved to Downloads",
            "local_path": downloads_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
