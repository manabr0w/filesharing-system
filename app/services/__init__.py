from .s3_service import S3Service
from app.config import settings

s3_service = S3Service(
    bucket_name=settings.AWS_BUCKET_NAME,
    region_name=settings.AWS_REGION,
    access_key=settings.AWS_ACCESS_KEY,
    secret_key=settings.AWS_SECRET_KEY,
)
