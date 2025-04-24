from uuid import UUID

from config import logger, settings
from src.api.grpc.connections.base import BaseConnection
from src.api.grpc.protobufs import profiles_pb2, profiles_pb2_grpc

logger = logger(__name__)


class ProfilesConnection(BaseConnection):
    def __init__(self, url: str):
        super().__init__(url)
        self.__stub = profiles_pb2_grpc.ProfilesServiceStub(self.channel)

    @property
    def stub(self) -> profiles_pb2_grpc.ProfilesServiceStub:
        return self.__stub

    async def create(
        self,
        account_id: UUID | str,
        first_name: str,
        last_name: str,
        age: int,
        gender: profiles_pb2.Gender | int,
        biography: str,
        image_base64_list: list[str],
        coordinates: dict[str, float],
        language_locale: str = 'ru',
    ) -> profiles_pb2.ProfileCreateResponse:
        if not isinstance(account_id, UUID):
            account_id = UUID(account_id)  # noqa: WPS125
        print(type(account_id), flush=True)
        print(type(first_name), flush=True)
        print(type(last_name), flush=True)
        print(type(age), flush=True)
        print(type(gender), flush=True)
        print(type(biography), flush=True)
        print(type(language_locale), flush=True)
        print(type(image_base64_list), flush=True)
        print(type(coordinates['lat']), flush=True)
        print(type(coordinates['lon']), flush=True)
        profile_request = profiles_pb2.ProfileCreateRequest(
            account_id=str(account_id),
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            biography=biography,
            language_locale=language_locale,
            image_base64_list=image_base64_list,
            lat=coordinates['lat'],
            lon=coordinates['lon'],
        )
        return self.stub.Create(profile_request)


profiles_connection = ProfilesConnection(settings.PROFILES_GRPC_URL)
