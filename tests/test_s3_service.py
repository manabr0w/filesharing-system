import pytest
from app.services.s3_service import S3Service
from fastapi import UploadFile
from io import BytesIO


class DummyS3Client:
    def __init__(self):
        self.uploaded_files = {}
        self.downloaded_files = {}

    def upload_fileobj(self, fileobj, bucket, key):
        content = fileobj.read()
        self.uploaded_files[key] = content

    def download_file(self, bucket, key, destination):
        if key not in self.uploaded_files:
            raise Exception("File not found")
        with open(destination, "wb") as f:
            f.write(self.uploaded_files[key])


@pytest.fixture
def dummy_service():
    service = S3Service(
        bucket_name="test-bucket",
        region_name="test-region",
        access_key="test-access",
        secret_key="test-secret"
    )
    service.s3 = DummyS3Client()
    return service


def test_upload_uploadfile_logic(dummy_service):
    content = b"hello world"
    file = UploadFile(filename="test.txt", file=BytesIO(content))

    import asyncio
    result = asyncio.run(dummy_service.upload_uploadfile(file, s3_key="test.txt"))

    assert result["message"] == "Upload successful"
    assert result["s3_key"] == "test.txt"
    assert dummy_service.s3.uploaded_files["test.txt"] == content


def test_download_file_logic(tmp_path, dummy_service):
    dummy_service.s3.uploaded_files["example.txt"] = b"sample content"
    dest = tmp_path / "example.txt"

    dummy_service.download_file("example.txt", str(dest))

    assert dest.exists()
    assert dest.read_bytes() == b"sample content"
