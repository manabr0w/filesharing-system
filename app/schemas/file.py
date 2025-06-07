from pydantic import BaseModel
from datetime import datetime


class FileMetadataBase(BaseModel):
    filename: str
    content_type: str | None = None
    size_bytes: int | None = None


class FileMetadataCreate(FileMetadataBase):
    set_id: str


class FileMetadataRead(FileMetadataBase):
    id: int
    set_id: str
    upload_timestamp: datetime

    class Config:
        orm_mode = True


class UploadResponse(BaseModel):
    message: str
    set_id: str
    uploaded_files: list[str]
