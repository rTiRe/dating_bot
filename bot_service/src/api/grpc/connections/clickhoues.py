from config import logger, settings
from src.api.grpc.connections.base import BaseConnection
from src.api.grpc.protobufs import clickhouse_pb2, clickhouse_pb2_grpc

logger = logger(__name__)


class ClickhouseConnection(BaseConnection):
    def __init__(self, url: str):
        super().__init__(url)
        self.__stub = clickhouse_pb2_grpc.ClickHouseServiceStub(self.channel)

    @property
    def stub(self) -> clickhouse_pb2_grpc.ClickHouseServiceStub:
        return self.__stub

    async def get_mutal_likes(
        self,
        user_id: str,
    ) -> clickhouse_pb2.GetUserMutualLikesResponse:
        likes_request = clickhouse_pb2.GetUserMutualLikesRequest(
            user_id=user_id,
        )
        return self.stub.GetUserMutualLikes(likes_request)


interactions_connection = ClickhouseConnection(settings.INTERACTIONS_GRPC_URL)
