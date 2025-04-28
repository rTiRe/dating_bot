import grpc

from src.api.grpc.protobufs import recommendations_pb2, recommendations_pb2_grpc, profiles_pb2

from src.storage.elasticsearch import database
from src.utils import search_cities, search_profiles


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
        try:
            profile_ids, total = await search_profiles(
                point={'lat': request.lat, 'lon': request.lon},
                age=request.age,
                gender=request.gender,
                distance=request.distance,
                prefer=request.prefer,
                limit=request.limit,
            )
        except Exception as exception:
            await context.abort(grpc.StatusCode.INTERNAL, str(exception))
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
            point = request.city_point
        else:
            point = request.user_point
            user_point_dict = {
                'lat': request.user_point.lat,
                'lon': request.user_point.lon,
            }
        try:
            cities, _total = await search_cities(
                lat=point.lat,
                lon=point.lon,
                distance=25,
                limit=1,
            )
        except Exception as exception:
            await context.abort(grpc.StatusCode.INTERNAL, str(exception))
        print(cities, flush=True)
        if cities:
            city_id = cities[0][0]
            city_point_dict = cities[0][1]
        if user_point_dict and not cities:
            city_id = ''
        document = {
            'city_point': city_point_dict,
            'user_point': user_point_dict,
            'age': request.age,
            'gender': request.gender,
            'rating': int(request.description_len > 0) * 20 + request.photo_count * 10,
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
        if city_id is not None:
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
