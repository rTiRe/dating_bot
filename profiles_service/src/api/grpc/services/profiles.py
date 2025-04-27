import base64
from uuid import UUID

import grpc
from asyncpg import UniqueViolationError

from config import logger
from src.api.grpc.protobufs.profiles import profiles_pb2, profiles_pb2_grpc
from src.api.grpc.protobufs.profiles.profiles_pb2 import UserPoint, CityPoint
from src.repositories.cities import CitiesRepository
from src.repositories.profiles import ProfilesRepository
from src.schemas.city import CreateCitySchema
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

    @staticmethod
    async def __check_gender(gender: int) -> None:
        if not gender:
            raise ValueError('The gender field must be set')

    @staticmethod
    async def __check_text(text: str) -> None:
        min_text_length = 0
        max_text_length = 2056
        if text and not (min_text_length <= len(text) <= max_text_length):
            raise ValueError(
                f'The length of the text field value must be from {min_text_length} to {max_text_length} characters',
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

    @staticmethod
    async def __check_city_point(city: CityPoint):
        if city and not (city.lat or city.lon or city.name):
            raise ValueError('The city point fields must all be set')

    @staticmethod
    async def __check_user_point(point: UserPoint):
        if point and not (point.lat or point.lon):
            raise ValueError('The user point fields must all be set')

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
        'city_point': __check_city_point,
        'user_point': __check_user_point,
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
        create_profile_schema = CreateProfileSchema(
            account_id=UUID(request.account_id),
            name=request.name,
            age=request.age,
            gender=request.gender,
            biography=request.biography,
            language_locale=request.language_locale,
            lat=request.user_point.lat,
            lon=request.user_point.lon,
            interested_in=request.interested_in,
            city_name=request.city_point.name,
        )
        async with database.pool.acquire() as connection:
            if request.city_point:
                create_city_schema = CreateCitySchema(lat=request.city_point.lat, lon=request.city_point.lon)
                try:
                    city = await CitiesRepository.create(connection, create_city_schema)
                except UniqueViolationError:
                    await context.abort(grpc.StatusCode.ALREADY_EXISTS)
                create_profile_schema.city_id = city.id
            try:
                profile = await ProfilesRepository.create(connection, create_profile_schema)
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
            rating=profile.rating,
            interested_in=profile.interested_in.name,
            city_point=CityPoint(lat=city.lat, lon=city.lon, name=profile.city_name),
        )


    async def Get(
        self,
        request: profiles_pb2.ProfilesGetRequest,
        context: grpc.aio.ServicerContext
    ) -> profiles_pb2.ProfilesGetResponse:
        profile_identifier = request.WhichOneof('identifier')
        if not profile_identifier:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                'The id or telegram_id field must be present',
            )
        try:
            await self.name_to_checker[profile_identifier](getattr(request, profile_identifier))
        except ValueError as exception:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exception))
        specification = EqualsSpecification(profile_identifier, getattr(request, profile_identifier))
        async with database.pool.acquire() as connection:
            profiles = (await ProfilesRepository.get(connection, specification))
            if len(profiles) == 0:
                await context.abort(grpc.StatusCode.NOT_FOUND, f'Profile {getattr(request, profile_identifier)} was not found')
            profile = profiles[0]
            city_specification = EqualsSpecification('id', str(profile.city_id))
            cities = (await CitiesRepository.get(connection, city_specification))
            if len(cities) == 0:
                await context.abort(grpc.StatusCode.NOT_FOUND, f'City {profile.id} was not found')
            city = cities[0]
        if not profile.image_names:
            profile.image_names.append(f'{minio_instance.default_name}{minio_instance.file_format}')
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
            rating=profile.rating,
            interested_in=profile.interested_in.name,
            city_point=CityPoint(lat=city.lat, lon=city.lon, name=profile.city_name),
            user_point=UserPoint(lat=profile.lat, lon=profile.lon),
        )

    async def GetList(
        self,
        request: profiles_pb2.ProfilesGetListRequest,
        context: grpc.aio.ServicerContext,
    ) -> profiles_pb2.ProfilesGetListResponse:
        profiles_identifiers = list(request.profiles_ids)
        for identifier in profiles_identifiers:
            try:
                await self.name_to_checker['id'](identifier)
            except ValueError as exception:
                await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exception))
        profiles_response: list[profiles_pb2.ProfilesGetResponse] = []
        async with database.pool.acquire() as connection:
            for identifier in profiles_identifiers:
                profile_specification = EqualsSpecification('id', identifier)
                profiles = (await ProfilesRepository.get(connection, profile_specification))
                if len(profiles) == 0:
                    await context.abort(grpc.StatusCode.NOT_FOUND, f'Profile {identifier} was not found')
                profile = profiles[0]
                city_specification = EqualsSpecification('id', str(profile.city_id))
                cities = (await CitiesRepository.get(connection, city_specification))
                if len(cities) == 0:
                    await context.abort(grpc.StatusCode.NOT_FOUND, f'City {profile.city_id} was not found')
                city = cities[0]
                if not profile.image_names:
                    profile.image_names.append(f'{minio_instance.default_name}{minio_instance.file_format}')
                image_base64_list = [
                    await ProfilesRepository.download_image(minio_instance, image_name)
                    for image_name in profile.image_names
                ]
                profiles_response.append(
                    profiles_pb2.ProfilesGetResponse(
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
                        rating=profile.rating,
                        interested_in=profile.interested_in.name,
                        city_point=CityPoint(
                            lat=city.lat,
                            lon=city.lon,
                            name=profile.city_name,
                        ),
                        user_point=UserPoint(
                            lat=profile.lat,
                            lon=profile.lon,
                        ),
                    )
                )
        return profiles_pb2.ProfilesGetListResponse(
            messages=profiles_response,
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
        update_result = 'UPDATE 0'
        async with database.pool.acquire() as connection:
            if any(update_schema.model_dump().values()) or not update_schema.biography is None:
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
