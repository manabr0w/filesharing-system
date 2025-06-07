from botocore.exceptions import BotoCoreError, ClientError
import boto3
from fastapi import UploadFile


class S3Service:
    def __init__(self, bucket_name: str, region_name: str, access_key: str, secret_key: str):
        self.bucket_name = bucket_name
        self.s3 = boto3.client(
            "s3",
            region_name=region_name,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    def download_file(self, s3_key: str, destination_path: str):
        try:
            self.s3.download_file(self.bucket_name, s3_key, destination_path)
        except (BotoCoreError, ClientError) as e:
            raise Exception(f"Download failed: {str(e)}")

    async def upload_files(self, files: list[UploadFile], set_id: str) -> list[str]:
        uploaded_keys = []
        try:
            for file in files:
                s3_key = f"{set_id}/{file.filename}"
                uploaded_keys.append(file.filename)

                await file.seek(0)
                self.s3.upload_fileobj(file.file, self.bucket_name, s3_key)

            return uploaded_keys
        except (BotoCoreError, ClientError) as e:
            raise Exception(f"S3 upload failed for set_id {set_id}: {str(e)}")
