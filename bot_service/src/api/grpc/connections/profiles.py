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
        interested_in: profiles_pb2.Gender | int,
        language_locale: str = 'ru',
        city_point: dict[str, float | str] | None = None,
        user_point: dict[str, float] | None = None,
    ) -> profiles_pb2.ProfileCreateResponse:
        if not isinstance(account_id, UUID):
            account_id = UUID(account_id)  # noqa: WPS125
        # print(image_base64_list, flush=True)
        profile_request = profiles_pb2.ProfileCreateRequest(
            account_id=str(account_id),
            name=name,
            age=age,
            gender=gender,
            biography=biography,
            language_locale=language_locale,
            image_base64_list=image_base64_list,
            interested_in=interested_in,
        )
        if city_point:
            profile_request.city_point.CopyFrom(profiles_pb2.CityPoint(**city_point))
        if user_point:
            profile_request.user_point.CopyFrom(profiles_pb2.UserPoint(**user_point))
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
        interested_in: profiles_pb2.Gender | int | None = None,
        language_locale: str | None = None,
        city_point: dict[str, float | str] | None = None,
        user_point: dict[str, float] | None = None,
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
                interested_in=interested_in,
            ),
        )
        if city_point:
            profile_request.data.city_point.CopyFrom(profiles_pb2.CityPoint(**city_point))
        if user_point:
            profile_request.data.user_point.CopyFrom(profiles_pb2.UserPoint(**user_point))
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

    async def get_by_profile_id(
        self,
        profile_id: UUID | str,
    ) -> profiles_pb2.ProfilesGetResponse:
        if not isinstance(profile_id, UUID):
            profile_id = UUID(profile_id)  # noqa: WPS125
        profile_request = profiles_pb2.ProfilesGetRequest(
            id=str(profile_id),
        )
        return self.stub.Get(profile_request)


profiles_connection = ProfilesConnection(settings.PROFILES_GRPC_URL)
