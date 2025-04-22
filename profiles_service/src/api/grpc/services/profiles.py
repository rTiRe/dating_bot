from uuid import UUID

import grpc
from asyncpg import UniqueViolationError

from config.logger import logger
from src.api.grpc.protobufs.profiles import profiles_pb2, profiles_pb2_grpc
from src.repositories.profiles import ProfilesRepository
from src.schemas.profile import UpdateProfileSchema, CreateProfileSchema
from src.specifications.equals import EqualsSpecification
from src.storage.postgres import database


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
            raise ValueError('The age field must be set')
        try:
            int(gender)
        except ValueError:
            raise ValueError('The age field must be of type Integer')
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

    name_to_checker = {
        'id': __check_id,
        'account_id': __check_id,
        'first_name': __check_name,
        'last_name': __check_name,
        'age': __check_age,
        'gender': __check_gender,
        'biography': __check_text,
        'additional_info': __check_text,
        'language': __check_language,
    }


    async def Create(
        self,
        request: profiles_pb2.ProfileCreateRequest,
        context: grpc.aio.ServicerContext,
    ) -> profiles_pb2.ProfileCreateResponse:
        try:
            for name, field_value in request.__dict__.items():
                await self.name_to_checker[name](field_value)
        except ValueError as exception:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exception))
        create_schema = CreateProfileSchema(
            account_id=UUID(request.account_id),
            first_name=request.first_name,
            last_name=request.last_name,
            age=request.age,
            gender=request.gender,
            biography=request.biography,
            additional_info=request.additional_info,
            language=request.language,
        )
        async with database.pool.acquire() as connection:
            try:
                profile = await ProfilesRepository.create(connection, create_schema)
            except UniqueViolationError:
                await context.abort(grpc.StatusCode.ALREADY_EXISTS)
        return profiles_pb2.ProfileCreateResponse(
            id=str(profile.id),
            account_id=str(profile.account_id),
            first_name=profile.first_name,
            last_name=profile.last_name,
            age=profile.age,
            gender=profile.gender,
            biography=profile.biography,
            additional_info=profile.additional_info,
            language=request.language,
            created_at=profile.created_at.isoformat(),
            updated_at=profile.updated_at.isoformat(),
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
        return profiles_pb2.ProfilesGetResponse(
            id=str(profile.id),
            account_id=str(profile.account_id),
            first_name=profile.first_name,
            last_name=profile.last_name,
            age=profile.age,
            gender=profile.gender.value,
            biography=profile.biography,
            additional_info=profile.additional_info,
            language=profile.language,
            created_at=profile.created_at.isoformat(),
            updated_at=profile.updated_at.isoformat(),
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
        return profiles_pb2.ProfilesDeleteResponse(result=delete_result)
