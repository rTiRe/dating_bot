import base64
import io
import time
from uuid import UUID

from asyncpg import Record
from asyncpg.connection import Connection
from minio.deleteobjects import DeleteObject
from pydantic import BaseModel

from src.exceptions import UpdateAllRowsException, ImageDeletionError
from src.repositories.base import BaseRepository
from src.schemas.profile import CreateProfileSchema, ProfileSchema, UpdateProfileSchema
from src.specifications.base import Specification
from src.storage.minio import MinIOConnection


class ProfilesRepository(BaseRepository):
    @staticmethod
    async def create(
        connection: Connection,
        create_data: CreateProfileSchema,
    ) -> ProfileSchema:
        data_dict = create_data.model_dump()
        data_dict['gender'] = str(data_dict['gender'].value)
        data_dict['interested_in'] = str(data_dict['interested_in'].value)
        statement_values = []
        columns = ', '.join([column for column in data_dict.keys()])
        values_pattern = ', '.join('??' for _ in range(len(data_dict)))
        statement_values.extend(list(data_dict.values()))
        statement = f"""
            insert into dating.profiles ({columns}) values ({values_pattern})
            returning *
        """
        statement = await Specification.to_asyncpg_query(f'{statement};')
        model_data: Record = await connection.fetchrow(statement, *statement_values)
        return ProfileSchema(**model_data)

    @staticmethod
    async def get(
        connection: Connection,
        *specifications: Specification,
        page: int = 1,
        page_size: int = 100,
    ) -> list[ProfileSchema]:
        return await super(__class__, __class__).get(
            connection,
            'dating.profiles',
            ProfileSchema,
            *specifications,
            page=page,
            page_size=page_size
        )

    @staticmethod
    async def update(
        connection: Connection,
        *specifications: Specification,
        update_all: bool = False,
        update_data: UpdateProfileSchema,
    ) -> str:
        if not specifications and not update_all:
            raise UpdateAllRowsException(
                f'You are trying to update all rows from a table dating.profiles. '
                'If you are sure, set update_all to True.'
            )
        update_values = update_data.model_dump(exclude_unset=True)
        if update_values.get('gender'):
            update_values['gender'] = str(update_values['gender'].value)
        if update_values.get('interested_in'):
            update_values['interested_in'] = str(update_values['interested_in'].value)
        set_statement = ', '.join([f'{column} = ??' for column in update_values.keys()])
        statement_values = list(update_values.values())
        statement = f'update dating.profiles set {set_statement}'
        if specifications:
            statement, statement_values = await BaseRepository.add_conditions(
                statement,
                statement_values,
                *specifications,
            )
        statement = await Specification.to_asyncpg_query(f'{statement};')
        return await connection.execute(statement, *statement_values)

    @staticmethod
    async def delete(
        connection: Connection,
        *specifications: Specification,
        delete_all: bool = False,
    ) -> str:
        return await super(__class__, __class__).delete(
            connection,
            'dating.profiles',
            *specifications,
            delete_all=delete_all,
        )

    @staticmethod
    async def upload_images(
        connection: Connection,
        minio: MinIOConnection,
        images: list[str],
        profile_id: UUID,
    ):
        files_names = []
        for idx, img_b64 in enumerate(images):
            try:
                img_data = base64.b64decode(img_b64)
            except ValueError:
                raise ValueError(f'Invalid base64 for image {idx}')
            timestamp = int(time.time()*1000)
            filename = f'{profile_id}_{timestamp}_{idx}{minio.file_format}'
            minio.client.put_object(
                bucket_name=minio.bucket,
                object_name=filename,
                data=io.BytesIO(img_data),
                length=len(img_data),
                content_type=minio.content_type,
            )
            files_names.append(filename)
        statement = f'update dating.profiles set image_names = ?? where id = ??'
        statement = await Specification.to_asyncpg_query(f'{statement};')
        return await connection.execute(statement, files_names, profile_id)

    @staticmethod
    async def download_image(
        minio: MinIOConnection,
        image_name: str,
    ) -> str | None:
        response = None
        image_base64 = None
        try:
            response = minio.client.get_object(
                bucket_name=minio.bucket,
                object_name=image_name
            )
        finally:
            if response:
                image_base64 = base64.b64encode(response.data).decode()
                response.close()
                response.release_conn()
        return image_base64

    @staticmethod
    async def delete_images(
        minio: MinIOConnection,
        profile_id: str,
    ) -> bool:
        images_list = map(
            lambda img: DeleteObject(img.object_name),
            minio.client.list_objects(
                bucket_name=minio.bucket,
                prefix=profile_id
            )
        )
        errors = minio.client.remove_objects(bucket_name=minio.bucket, delete_object_list=images_list)
        if errors:
            for error in errors:
                raise ImageDeletionError(f'{error.name}: {error.message}')
        return True