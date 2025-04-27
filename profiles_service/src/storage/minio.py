import base64
import io

from minio import Minio

from config import settings


class MinIOConnection:
    def __init__(self, minio_client: Minio):
        self.client = minio_client
        self.bucket = settings.MINIO_BUCKET
        self.default_name = 'placeholder_image'
        self.file_format = '.jpg'
        self.content_type = "image/jpeg"
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)
        # self.add_placeholder_image()

    # def add_placeholder_image(self):
    #     with open("src/static/placeholder_image.jpg", "rb") as image_file:
    #         img_data = base64.b64encode(image_file.read())
    #         print(img_data, flush=True)
    #         self.client.put_object(
    #             bucket_name=self.bucket,
    #             object_name=f'{self.default_name}{self.file_format}',
    #             data=io.BytesIO(img_data),
    #             length=len(img_data),
    #             content_type=self.content_type,
    #         )

minio_instance = MinIOConnection(Minio(
    endpoint=settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
))
