import base64
from uuid import UUID

import grpc
from asyncpg import UniqueViolationError

from config import logger
from src.api.grpc.protobufs.profiles import profiles_pb2, profiles_pb2_grpc
from src.repositories.profiles import ProfilesRepository
from src.schemas.profile import UpdateProfileSchema, CreateProfileSchema
from src.specifications.equals import EqualsSpecification
from src.storage.minio import minio_instance
from src.storage.postgres import database

logger = logger(__name__)

class ProfilesService(profiles_pb2_grpc.ProfilesServiceServicer):
    @staticmethod
    async def serve() -> None:
        server = grpc.aio.server()
        profiles_pb2_grpc.add_ProfilesServiceServicer_to_server(ProfilesService(), server)
        server.add_insecure_port('[::]:1337')
        await server.start()
        await server.wait_for_termination()

    @staticmethod
    async def __check_id(id: str | UUID) -> None:
        if not id:
            raise ValueError('The id field must be set')
        try:
            UUID(id)
        except ValueError:
            raise ValueError('The id field must be of type UUID')

    @staticmethod
    async def __check_name(name: str) -> None:
        if not name:
            raise ValueError('The name field must be set')

    @staticmethod
    async def __check_age(age: int) -> None:
        if not age:
            raise ValueError('The age field must be set')
        try:
            int(age)
        except ValueError:
            raise ValueError('The age field must be of type Integer')

    @staticmethod
    async def __check_gender(gender: int) -> None:
        if not gender:
            raise ValueError('The gender field must be set')
        try:
            int(gender)
        except ValueError:
            raise ValueError('The gender field must be of type Integer')
        if abs(int(gender)) > 2:
            raise ValueError('There are only two genders, faggot')

    @staticmethod
    async def __check_text(text: str) -> None:
        min_text_length = 0
        max_text_length = 256
        if text and not (min_text_length <= len(text) <= max_text_length):
            raise ValueError(
                'The length of the text field value must be from 0 to 256 characters',
            )

    @staticmethod
    async def __check_language(lang: str) -> None:
        if not lang:
            raise ValueError('The language field must be set')
        if len(lang) > 2:
            raise ValueError('The language code must conform to the ISO 639-1 format (two-character code)')

    @staticmethod
    async def __check_image_base64_list(images: list[str]):
        for idx, image_str in enumerate(images):
            try:
                base64.b64decode(image_str)
            except ValueError:
                raise ValueError(f'The image {idx} string must be valid base64')

    @staticmethod
    async def __check_coordinates(coordinate: float):
        if not coordinate:
            raise ValueError('The coordinates fields must be set')

    name_to_checker = {
        'id': __check_id,
        'account_id': __check_id,
        'name': __check_name,
        'age': __check_age,
        'gender': __check_gender,
        'biography': __check_text,
        'language_locale': __check_language,
        'image_base64_list': __check_image_base64_list,
        'lat': __check_coordinates,
        'lon': __check_coordinates,
        'interested_in': __check_gender,
    }


    async def Create(
        self,
        request: profiles_pb2.ProfileCreateRequest,
        context: grpc.aio.ServicerContext,
    ) -> profiles_pb2.ProfileCreateResponse:
        try:
            for descriptor, field_value in request.ListFields():
                await self.name_to_checker[descriptor.name](field_value)
        except ValueError as exception:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exception))
        create_schema = CreateProfileSchema(
            account_id=UUID(request.account_id),
            name=request.name,
            age=request.age,
            gender=request.gender,
            biography=request.biography,
            language_locale=request.language_locale,
            lat=request.lat,
            lon=request.lon,
            interested_in=request.interested_in
        )
        async with database.pool.acquire() as connection:
            try:
                profile = await ProfilesRepository.create(connection, create_schema)
            except UniqueViolationError:
                await context.abort(grpc.StatusCode.ALREADY_EXISTS)
            try:
                await ProfilesRepository.upload_images(
                    connection,
                    minio_instance,
                    list(request.image_base64_list),
                    profile.id,
                )
            except Exception as exception:
                logger.exception(exception)
                await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exception))
        return profiles_pb2.ProfileCreateResponse(
            id=str(profile.id),
            account_id=str(profile.account_id),
            name=profile.name,
            age=profile.age,
            gender=profile.gender.name,
            biography=profile.biography,
            language_locale=request.language_locale,
            created_at=profile.created_at.isoformat(),
            updated_at=profile.updated_at.isoformat(),
            lat=profile.lat,
            lon=profile.lon,
            rating=profile.rating,
        )


    async def Get(
        self,
        request: profiles_pb2.ProfilesGetRequest,
        context: grpc.aio.ServicerContext
    ) -> profiles_pb2.ProfilesGetResponse:
        identifier_field = request.WhichOneof('identifier')
        if not identifier_field:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                'The id or telegram_id field must be present',
            )
        try:
            await self.name_to_checker[identifier_field](getattr(request, identifier_field))
        except ValueError as exception:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exception))
        specification = EqualsSpecification(identifier_field, getattr(request, identifier_field))
        async with database.pool.acquire() as connection:
            profiles = (await ProfilesRepository.get(connection, specification))
            if len(profiles) == 0:
                await context.abort(grpc.StatusCode.NOT_FOUND)
            profile = profiles[0]
        image_base64_list = [await ProfilesRepository.download_image(minio_instance, image_name) for image_name in profile.image_names]
        return profiles_pb2.ProfilesGetResponse(
            id=str(profile.id),
            account_id=str(profile.account_id),
            name=profile.name,
            age=profile.age,
            gender=profile.gender.name,
            biography=profile.biography,
            language_locale=profile.language_locale,
            created_at=profile.created_at.isoformat(),
            updated_at=profile.updated_at.isoformat(),
            image_base64_list=image_base64_list,
            lat=profile.lat,
            lon=profile.lon,
            rating=profile.rating,
            interested_in=profile.interested_in.name,
        )

    async def Update(
        self,
        request: profiles_pb2.ProfileUpdateRequest,
        context: grpc.aio.ServicerContext,
    ) -> profiles_pb2.ProfilesUpdateResponse:
        update_data = {descriptor.name: field_value for descriptor, field_value in request.data.ListFields()}
        if not update_data:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, 'Empty update data')
        for name, field_value in update_data.items():
            try:  # noqa: WPS229
                await self.__check_id(request.id)
                await self.name_to_checker[name](field_value)
            except ValueError as exception:
                await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exception))
        specification = EqualsSpecification('id', request.id)
        update_schema = UpdateProfileSchema(**update_data)
        async with database.pool.acquire() as connection:
            if any(update_schema.model_dump().values()):
                try:
                    update_result = await ProfilesRepository.update(
                        connection,
                        specification,
                        update_data=update_schema,
                    )
                except UniqueViolationError as exception:
                    logger.error(exception)
                    await context.abort(
                        grpc.StatusCode.ALREADY_EXISTS,
                        'An account with this telegram_id field already exists',
                    )
            if update_data.get('image_base64_list'):
                try:
                    await ProfilesRepository.delete_images(minio_instance, request.id)
                    update_result = await ProfilesRepository.upload_images(
                        connection,
                        minio_instance,
                        update_data['image_base64_list'],
                        UUID(request.id),
                    )
                except Exception as exception:
                    logger.exception(exception)
                    await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exception))
        return profiles_pb2.ProfilesUpdateResponse(result=update_result)

    async def Delete(
        self,
        request: profiles_pb2.ProfileDeleteRequest,
        context: grpc.aio.ServicerContext,
    ) -> profiles_pb2.ProfilesDeleteResponse:
        try:
            await self.__check_id(request.id)
        except ValueError as exception:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exception))
        delete_specification = EqualsSpecification('id', request.id)
        async with database.pool.acquire() as connection:
            delete_result = await ProfilesRepository.delete(connection, delete_specification)
        await ProfilesRepository.delete_images(minio_instance, request.id)
        return profiles_pb2.ProfilesDeleteResponse(result=delete_result)
