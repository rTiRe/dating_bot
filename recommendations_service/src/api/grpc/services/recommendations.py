import grpc

from src.api.grpc.protobufs import recommendations_pb2, recommendations_pb2_grpc

from src.storage.elasticsearch import database


class RecommendationsService(recommendations_pb2_grpc.RecommendationsServiceServicer):
    @staticmethod
    async def serve():
        server = grpc.aio.server() # type: ignore
        recommendations_pb2_grpc.add_ElasticSearchServicer_to_server(RecommendationsService(), server) # type: ignore
        server.add_insecure_port('[::]:1337')
        await server.start()
        await server.wait_for_termination()

    async def GetMatch(
        self,
        request: recommendations_pb2.RecommendationsGetMatchRequest,
        context: grpc.aio.ServicerContext, # type: ignore
    ) -> recommendations_pb2.RecommendationsGetMatchResponse:
        query = {
            'query': {
                'bool': {
                    'must': [
                        {'term': {'gender': request.gender}},
                        {'range': {'age': {'gte': request.age_min, 'lte': request.age_max}}},
                    ],
                    'filter': {
                        'geo_distance': {
                            'distance': f'{request.distance}km',
                            'location': {'lat': request.lat, 'lon': request.lon},
                        },
                    },
                },
            },
            'size': request.limit,
        }
        try:
            response = database.elasticsearch.search(index='users', body=query)
        except Exception as exception:
            context.abort(grpc.StatusCode.INTERNAL, str(exception))
        hits = response['hits']['hits']
        user_ids = [hit['_source']['user_id'] for hit in hits]
        total = response['hits']['total']['value']
        return recommendations_pb2.RecommendationsGetMatchResponse(
            user_ids=user_ids,
            total=total
        )

    async def UpdateUser(
        self,
        request: recommendations_pb2.RecommendationsUpdateUserRequest,
        context: grpc.aio.ServicerContext, # type: ignore
    ) -> recommendations_pb2.RecommendationsUpdateUserResponse:
        doc = {
            'user_id': request.user_id,
            'location': {
                'lat': request.lat,
                'lon': request.lon
            },
            'age': request.age,
            'gender': request.gender
        }
        try:
            response = database.elasticsearch.index(
                index='users',
                id=request.user_id,
                body=doc,
                op_type='index'
            )
        except Exception as exception:
            context.abort(grpc.StatusCode.INTERNAL, str(exception))
        created = response['result'] == 'created'
        return recommendations_pb2.RecommendationsUpdateUserResponse(
            user_id=request.user_id,
            created=created
        )
