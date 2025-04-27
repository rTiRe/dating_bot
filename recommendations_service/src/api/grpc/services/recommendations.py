import grpc

from src.api.grpc.protobufs import recommendations_pb2, recommendations_pb2_grpc, profiles_pb2

from src.storage.elasticsearch import database
from src.utils import search_cities


class RecommendationsService(recommendations_pb2_grpc.RecommendationsServiceServicer):
    @staticmethod
    async def serve():
        server = grpc.aio.server()
        recommendations_pb2_grpc.add_RecommendationsServiceServicer_to_server(RecommendationsService(), server)
        server.add_insecure_port('[::]:1337')
        await server.start()
        await server.wait_for_termination()

    async def SearchProfiles(
        self,
        request: recommendations_pb2.RecommendationsSearchProfilesRequest,
        context: grpc.aio.ServicerContext,
    ) -> recommendations_pb2.RecommendationsSearchProfilesResponse:
        query = {
            'query': {
                'bool': {
                    'must': [
                        # {'term': {'gender': request.gender}},
                        # {'range': {'age': {'gte': request.age_min, 'lte': request.age_max}}},
                        {'match_all': {}},
                    ],
                    # 'filter': {
                    #     'geo_distance': {
                    #         'distance': f'{request.distance}km',
                    #         'location': {'lat': request.lat, 'lon': request.lon},
                    #     },
                    # },
                },
            },
            'size': request.limit,
        }
        try:
            response = await database.elasticsearch.search(index='profiles', body=query)
        except Exception as exception:
            await context.abort(grpc.StatusCode.INTERNAL, str(exception))
        hits = response['hits']['hits']
        profile_ids = [hit['_id'] for hit in hits]
        total = response['hits']['total']['value']
        return recommendations_pb2.RecommendationsSearchProfilesResponse(
            profile_ids=profile_ids,
            total=total
        )

    async def UpdateProfile(
        self,
        request: recommendations_pb2.RecommendationsUpdateProfileRequest,
        context: grpc.aio.ServicerContext,
    ) -> recommendations_pb2.RecommendationsUpdateProfileResponse:
        city_id = None
        city_point_dict = None
        user_point_dict = None
        if request.HasField('city_point'):
            city_point_dict = {
                'lat': request.city_point.lat,
                'lon': request.city_point.lon,
            }
        if request.HasField('user_point'):
            try:
                cities, _total = await search_cities(
                    lat=request.user_point.lat,
                    lon=request.user_point.lon,
                    distance=25,
                    limit=1,
                )
            except Exception as exception:
                await context.abort(grpc.StatusCode.INTERNAL, str(exception))
            user_point_dict = {
                'lat': request.user_point.lat,
                'lon': request.user_point.lon,
            }
            if cities:
                city_id = cities[0][0]
                city_point_dict = cities[0][1]
        document = {
            'city_point': city_point_dict,
            'user_point': user_point_dict,
            'age': request.age,
            'gender': request.gender,
        }
        try:
            profile_response = await database.elasticsearch.index(
                index='profiles',
                id=request.profile_id,
                body=document,
                op_type='index'
            )
        except Exception as exception:
            await context.abort(grpc.StatusCode.INTERNAL, str(exception))
        response_message = recommendations_pb2.RecommendationsUpdateProfileResponse(
            profile_id=request.profile_id,
            age=request.age,
            gender=request.gender,
            result=profile_response['result'],
        )
        if city_id:
            response_message.city_id = city_id
        if city_point_dict:
            response_message.city_point.CopyFrom(profiles_pb2.CityPoint(name='', **city_point_dict))
        if user_point_dict:
            response_message.user_point.CopyFrom(profiles_pb2.UserPoint(**user_point_dict))
        return response_message

    async def UpdateCity(
        self,
        request: recommendations_pb2.RecommendationsUpdateCityRequest,
        context: grpc.aio.ServicerContext,
    ) -> recommendations_pb2.RecommendationsUpdateCityResponse:
        document = {
            'point': {
                'lat': request.lat,
                'lon': request.lon,
            },
        }
        try:
            response = await database.elasticsearch.index(
                index='cities',
                id=request.city_id,
                document=document,
                op_type='index',
            )
        except Exception as exception:
            await context.abort(grpc.StatusCode.INTERNAL, str(exception))
        return recommendations_pb2.RecommendationsUpdateCityResponse(
            city_id=request.city_id,
            result=response['result'],
        )

    async def SearchCities(
        self,
        request: recommendations_pb2.RecommendationsSearchCitiesRequest,
        context: grpc.aio.ServicerContext,
    ) -> recommendations_pb2.RecommendationsSearchCitiesResponse:
        try:
            cities, total = await search_cities(
                lat=request.lat,
                lon=request.lon,
                distance=request.distance,
                limit=request.limit,
            )
        except Exception as exception:
            await context.abort(grpc.StatusCode.INTERNAL, str(exception))
        city_ids = [city_id for city_id, _city_point in cities]
        return recommendations_pb2.RecommendationsSearchCitiesResponse(
            city_ids=city_ids,
            total=total,
        )
