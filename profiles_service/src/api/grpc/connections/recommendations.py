from uuid import UUID


from src.api.grpc.connections.base import BaseConnection
from config import logger, settings
from src.api.grpc.protobufs.profiles import profiles_pb2
from src.api.grpc.protobufs.profiles.profiles_pb2 import UserPoint
from src.api.grpc.protobufs.recommendations import recommendations_pb2_grpc, recommendations_pb2
from src.schemas.profile import CityPoint

logger = logger(__name__)


class RecommendationsConnection(BaseConnection):
    def __init__(self, url: str):
        super().__init__(url)
        self.__stub = recommendations_pb2_grpc.RecommendationsServiceStub(self.channel)

    @property
    def stub(self) -> recommendations_pb2_grpc.RecommendationsServiceStub:
        return self.__stub

    async def update_profile(
        self,
        profile_id: UUID | None = None,
        age: int | None = None,
        gender: profiles_pb2.Gender | None = None,
        city_point: CityPoint | None = None,
        user_point: UserPoint | None = None,
    ) -> recommendations_pb2.RecommendationsUpdateProfileResponse:
        if profile_id and not isinstance(profile_id, UUID):
            profile_id = str(UUID(profile_id))  # noqa: WPS125
        update_request = recommendations_pb2.RecommendationsUpdateProfileResponse(
            profile_id=str(profile_id),
            age=age,
            gender=gender,
            city_point=city_point,
            user_point=user_point
        )
        return self.stub.UpdateProfile(update_request)

    async def update_city(
        self,
        city_id: UUID | None = None,
        lat: float | None = None,
        lon: float | None = None,
    ) -> recommendations_pb2.RecommendationsUpdateCityResponse:
        if city_id and not isinstance(city_id, UUID):
            city_id = str(UUID(city_id))  # noqa: WPS125
        update_request = recommendations_pb2.RecommendationsUpdateCityResponse(
            city_id=str(city_id),
            lat=lat,
            lon=lon,
        )
        return self.stub.UpdateCity(update_request)


recommendations_connection = RecommendationsConnection(settings.RECOMMENDATIONS_GRPC_URL)