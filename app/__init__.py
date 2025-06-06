from app.config import settings
from app.services.s3_service import S3Service

s3_service = S3Service(
    bucket_name=settings.aws_bucket_name,
    region_name=settings.aws_region,
    access_key=settings.aws_access_key,
    secret_key=settings.aws_secret_key,
)
