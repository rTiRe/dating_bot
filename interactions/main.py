import asyncio
import clickhouse_connect
import grpc
from concurrent import futures
import proto.clickhouse_pb2 as clickhouse_pb2
import proto.clickhouse_pb2_grpc as clickhouse_pb2_grpc
from datetime import datetime

class ClickHouseServicer(clickhouse_pb2_grpc.ClickHouseServiceServicer):
    def __init__(self):
        self.client = None

    async def setup(self):
        self.client = await clickhouse_connect.get_async_client(
            host="clickhouse_instance",
            port=8123,
            username="default",
            password="default"
        )

    async def GetUserInteractions(self, request, context):
        query = f"""
        SELECT timestamp, liker_id, liked_id, interaction_type
        FROM dating.interactions
        WHERE liker_id = '{request.user_id}'
        """
        result = await self.client.query(query)

        interactions = []
        for row in result.result_set:
            interaction = clickhouse_pb2.Interaction(
                timestamp=row[0].isoformat(),
                liker_id=str(row[1]),
                liked_id=str(row[2]),
                interaction_type=row[3]
            )
            interactions.append(interaction)

        return clickhouse_pb2.GetUserInteractionsResponse(interactions=interactions)

    async def GetUserReceivedLikes(self, request, context):
        query = f"""
        SELECT timestamp, liker_id, liked_id
        FROM dating.interactions
        WHERE liked_id = '{request.user_id}' AND interaction_type = 'like'
        """
        result = await self.client.query(query)

        likes = []
        for row in result.result_set:
            like = clickhouse_pb2.Like(
                timestamp=row[0].isoformat(),
                liker_id=str(row[1]),
                liked_id=str(row[2])
            )
            likes.append(like)

        return clickhouse_pb2.GetUserReceivedLikesResponse(likes=likes)

    async def GetUserReceivedDislikes(self, request, context):
        query = f"""
        SELECT timestamp, liker_id, liked_id
        FROM dating.interactions
        WHERE liked_id = '{request.user_id}' AND interaction_type = 'dislike'
        """
        result = await self.client.query(query)

        dislikes = []
        for row in result.result_set:
            dislike = clickhouse_pb2.Dislike(
                timestamp=row[0].isoformat(),
                disliker_id=str(row[1]),
                disliked_id=str(row[2])
            )
            dislikes.append(dislike)

        return clickhouse_pb2.GetUserReceivedDislikesResponse(dislikes=dislikes)

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = ClickHouseServicer()
    await servicer.setup()

    clickhouse_pb2_grpc.add_ClickHouseServiceServicer_to_server(servicer, server)
    server.add_insecure_port('[::]:1337')
    await server.start()
    print("Server started on port 1337")
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())
