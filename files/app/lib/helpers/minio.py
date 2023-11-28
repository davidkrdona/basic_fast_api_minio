from io import BytesIO

from minio import Minio
import os


class MinioHelper:
    def __init__(self, bucket_name):
        # Need to set up the docker
        self.minio_client = Minio(
            "localhost:9000",
            access_key=os.environ.get("MINIO_ROOT_USER", "minio_admin"),
            secret_key=os.environ.get("MINIO_ROOT_PASSWORD", "minio_password"),
            secure=False,  # Change to True if using HTTPS
        )

        self.bucket_name = bucket_name

    def check_bucket(self, create_if_no_exist=True):
        """Creates a bucket if it doesn't exist."""
        if not self.minio_client.bucket_exists(self.bucket_name) and create_if_no_exist:
            self.minio_client.make_bucket(self.bucket_name)

    def upload_object(self, file, object_name):
        """Uploads file to a bucket."""
        file_data = file.file.read()
        file_name = object_name or file.filename
        file_size = len(file_data)
        content_type = file.content_type

        self.minio_client.put_object(
            self.bucket_name,
            object_name=file_name,
            data=BytesIO(file_data),
            length=file_size,
            content_type=content_type,
        )
        return file_name
