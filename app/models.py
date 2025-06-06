from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class FileMetadata(Base):
    __tablename__ = "file_metadata"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    s3_rec_id = Column(String, unique=True, index=True)
    content_type = Column(String, nullable=True)
    size_bytes = Column(BigInteger, nullable=True)
    upload_timestamp = Column(DateTime(timezone=True), server_default=func.now())
