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
        searcher_id: str,
        city_point: dict[str, float] | None = None,
        user_point: dict[str, float] | None = None,
        distance: float = 25,
        limit: int = 10,
    ) -> recommendations_pb2.RecommendationsSearchProfilesResponse:
        profile_request = recommendations_pb2.RecommendationsSearchProfilesRequest(
            age=age,
            gender=gender,
            distance=distance,
            limit=limit,
            searcher_id=searcher_id,
        )
        if user_point:
            profile_request.lat, profile_request.lon = user_point['lat'], user_point['lon']
            profile_request.prefer = 'user'
        else:
            profile_request.lat, profile_request.lon = city_point['lat'], city_point['lon']
            profile_request.prefer = 'city'
        return self.stub.SearchProfiles(profile_request)


recommendations_connection = RecommendationsConnection(settings.RECOMMENDATIONS_GRPC_URL)
