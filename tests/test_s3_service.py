import pytest
from app.services.s3_service import S3Service
from fastapi import UploadFile
from io import BytesIO


class DummyS3Client:
    """Спрощений фейковий клієнт для тестування логіки без реального AWS"""
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
    service.s3 = DummyS3Client()  # замінюємо boto3 клієнт
    return service


def test_upload_files_logic(dummy_service):
    set_id = "test-set-123"
    content1 = b"hello world"
    content2 = b"goodbye world"
    files_to_upload = [
        UploadFile(filename="test1.txt", file=BytesIO(content1)),
        UploadFile(filename="test2.log", file=BytesIO(content2)),
    ]

    result_keys = dummy_service.upload_files(files_to_upload, set_id)

    expected_keys = [f"{set_id}/test1.txt", f"{set_id}/test2.log"]
    assert result_keys == expected_keys

    assert dummy_service.s3.uploaded_files[expected_keys[0]] == content1
    assert dummy_service.s3.uploaded_files[expected_keys[1]] == content2


def test_download_file_logic(tmp_path, dummy_service):
    dummy_service.s3.uploaded_files["example.txt"] = b"sample content"
    dest = tmp_path / "example.txt"

    dummy_service.download_file("example.txt", str(dest))

    assert dest.exists()
    assert dest.read_bytes() == b"sample content"
