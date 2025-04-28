from config import logger, settings
from src.api.grpc.connections.base import BaseConnection
from src.api.grpc.protobufs import recommendations_pb2, recommendations_pb2_grpc, profiles_pb2

logger = logger(__name__)


class RecommendationsConnection(BaseConnection):
    def __init__(self, url: str):
        super().__init__(url)
        self.__stub = recommendations_pb2_grpc.RecommendationsServiceStub(self.channel)

    @property
    def stub(self) -> recommendations_pb2_grpc.RecommendationsServiceStub:
        return self.__stub

    async def search_profiles(
        self,
        gender: profiles_pb2.Gender | int,
        age: int,
        city_point: profiles_pb2.CityPoint | None = None,
        user_point: profiles_pb2.UserPoint | None = None,
        distance: float = 25,
        limit: int = 10,
    ) -> recommendations_pb2.RecommendationsSearchProfilesResponse:
        profile_request = recommendations_pb2.RecommendationsSearchProfilesRequest(
            age=age,
            gender=gender,
        )
        return self.stub.Create(profile_request)


recommendations_connection = RecommendationsConnection(settings.RECOMMENDATIONS_GRPC_URL)
