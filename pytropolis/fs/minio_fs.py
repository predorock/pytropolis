from minio import Minio
from minio.error import ResponseError

class MinIOFileManager:
    def __init__(self, access_key, secret_key, endpoint, secure=True):
        """
        Initialize MinIO client.
        :param access_key: MinIO access key.
        :param secret_key: MinIO secret key.
        :param endpoint: MinIO server endpoint URL.
        :param secure: Use HTTPS (default: True).
        """
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )

    def create_bucket(self, bucket_name):
        """
        Create a bucket.
        :param bucket_name: Name of the bucket to create.
        :return: None
        """
        try:
            self.client.make_bucket(bucket_name)
        except ResponseError as err:
            print(err)

    def upload_file(self, bucket_name, object_name, file_path):
        """
        Upload a file to a bucket.
        :param bucket_name: Name of the bucket to upload to.
        :param object_name: Name of the object to upload.
        :param file_path: Path to the file to upload.
        :return: None
        """
        try:
            self.client.fput_object(bucket_name, object_name, file_path)
        except ResponseError as err:
            print(err)

    def download_file(self, bucket_name, object_name, download_path):
        """
        Download a file from a bucket.
        :param bucket_name: Name of the bucket to download from.
        :param object_name: Name of the object to download.
        :param download_path: Path to download the file to.
        :return: None
        """
        try:
            self.client.fget_object(bucket_name, object_name, download_path)
        except ResponseError as err:
            print(err)

    def update_file(self, bucket_name, object_name, new_file_path):
        """
        Update a file in a bucket.
        :param bucket_name: Name of the bucket to update.
        :param object_name: Name of the object to update.
        :param new_file_path: Path to the new file to update with.
        :return: None
        """
        try:
            self.client.fput_object(bucket_name, object_name, new_file_path)
        except ResponseError as err:
            print(err)

    def delete_file(self, bucket_name, object_name):
        """
        Delete a file from a bucket.
        :param bucket_name: Name of the bucket to delete from.
        :param object_name: Name of the object to delete.
        :return: None
        """
        try:
            self.client.remove_object(bucket_name, object_name)
        except ResponseError as err:
            print(err)

    def delete_bucket(self, bucket_name):
        """
        Delete a bucket.
        :param bucket_name: Name of the bucket to delete.
        :return: None
        """
        try:
            self.client.remove_bucket(bucket_name)
        except ResponseError as err:
            print(err)

    def list_buckets(self):
        """
        List all buckets.
        :return: List of buckets.
        """
        try:
            return self.client.list_buckets()
        except ResponseError as err:
            print(err)

    def close(self):
        """
        Close the connection.
        :return: None
        """
        self.client.close()
