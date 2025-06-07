import os
import shortuuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.models import FileMetadata
from app.schemas.file import UploadResponse, FileMetadataCreate
from app.services import s3_service

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_files(files: list[UploadFile] = File(...), db: AsyncSession = Depends(get_db_session)):
    try:
        set_id = shortuuid.uuid()

        async with db.begin():
            for file in files:
                metadata = FileMetadataCreate(
                    set_id=set_id,
                    filename=file.filename,
                    content_type=file.content_type,
                    size_bytes=file.size
                )
                db.add(FileMetadata(**metadata.dict()))
            await db.commit()

        uploaded_s3_keys = await s3_service.upload_files(files, set_id)

        return {
            "message": "Upload successful",
            "set_id": set_id,
            "uploaded_files": uploaded_s3_keys
        }

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")


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
