from minio import Minio

from config import settings


class MinIOConnection:
    def __init__(self, minio_client: Minio):
        self.client = minio_client
        self.bucket = settings.MINIO_BUCKET
        # print(self.client.bucket_exists(self.bucket), flush=True)
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

minio_instance = MinIOConnection(Minio(
    endpoint=settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
))