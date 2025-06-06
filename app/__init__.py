from app.config import settings
from app.services.s3_service import S3Service

s3_service = S3Service(
    bucket_name=settings.AWS_BUCKET_NAME,
    region_name=settings.AWS_REGION,
    access_key=settings.AWS_ACCESS_KEY,
    secret_key=settings.AWS_SECRET_KEY,
)
