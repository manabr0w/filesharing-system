import boto3
from botocore.exceptions import BotoCoreError, ClientError
import os

class S3Service:
    def __init__(self, bucket_name: str, region_name: str, access_key: str, secret_key: str):
        self.bucket_name = bucket_name
        self.s3 = boto3.client(
            "s3",
            region_name=region_name,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    def upload_file(self, file_path: str, s3_key: str):
        try:
            self.s3.upload_file(file_path, self.bucket_name, s3_key)
            return {"message": "Upload successful", "s3_key": s3_key}
        except (BotoCoreError, ClientError) as e:
            raise Exception(f"Upload failed: {str(e)}")

    def download_file(self, s3_key: str, destination_path: str):
        try:
            self.s3.download_file(self.bucket_name, s3_key, destination_path)
            return {"message": "Download successful", "local_path": destination_path}
        except (BotoCoreError, ClientError) as e:
            raise Exception(f"Download failed: {str(e)}")
