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
        name: str,
        age: int,
        gender: profiles_pb2.Gender | int,
        biography: str,
        image_base64_list: list[str],
        coordinates: dict[str, float],
        interested_in: profiles_pb2.Gender | int,
        language_locale: str = 'ru',
    ) -> profiles_pb2.ProfileCreateResponse:
        if not isinstance(account_id, UUID):
            account_id = UUID(account_id)  # noqa: WPS125
        profile_request = profiles_pb2.ProfileCreateRequest(
            account_id=str(account_id),
            name=name,
            age=age,
            gender=gender,
            biography=biography,
            language_locale=language_locale,
            image_base64_list=image_base64_list,
            lat=coordinates['lat'],
            lon=coordinates['lon'],
            interested_in=interested_in,
        )
        return self.stub.Create(profile_request)

    async def update(
        self,
        id: UUID | str,
        account_id: UUID | str | None = None,
        name: str | None = None,
        age: int | None = None,
        gender: profiles_pb2.Gender | int | None = None,
        biography: str | None = None,
        image_base64_list: list[str] | None = None,
        coordinates: dict[str, float] = {},
        interested_in: profiles_pb2.Gender | int | None = None,
        language_locale: str | None = None,
    ) -> profiles_pb2.ProfilesUpdateResponse:
        if not isinstance(id, UUID):
            id = UUID(id)  # noqa: WPS125
        if account_id and not isinstance(account_id, UUID):
            account_id = str(UUID(account_id))  # noqa: WPS125
        profile_request = profiles_pb2.ProfileUpdateRequest(
            id=str(id),
            data=profiles_pb2.ProfileUpdateRequest.UpdateData(
                account_id=account_id,
                name=name,
                age=age,
                gender=gender,
                biography=biography,
                language_locale=language_locale,
                image_base64_list=image_base64_list,
                lat=coordinates.get('lat'),
                lon=coordinates.get('lon'),
                interested_in=interested_in,
            ),
        )
        return self.stub.Update(profile_request)

    async def get_by_account_id(
        self,
        account_id: UUID | str,
    ) -> profiles_pb2.ProfilesGetResponse:
        if not isinstance(account_id, UUID):
            account_id = UUID(account_id)  # noqa: WPS125
        profile_request = profiles_pb2.ProfilesGetRequest(
            account_id=str(account_id),
        )
        return self.stub.Get(profile_request)


profiles_connection = ProfilesConnection(settings.PROFILES_GRPC_URL)
