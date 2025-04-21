from uuid import UUID

import grpc

from src.api.grpc.protobufs.profiles import profiles_pb2, profiles_pb2_grpc
from src.specifications.equals import EqualsSpecification
from src.storage.postgres import database


class ProfilesService(profiles_pb2_grpc.ProfilesServiceServicer):
    @staticmethod
    async def serve() -> None:
        server = grpc.aio.server()
        profiles_pb2_grpc.add_ProfilesServiceServicer_to_server(ProfilesService(), server)
        server.add_insecure_port('[::]:1337')
        await server.start()
        await server.wait_for_termination()

    @staticmethod
    async def __check_id(id: str | UUID) -> None:
        if not id:
            raise ValueError('The id field must be set')
        try:
            UUID(id)
        except ValueError:
            raise ValueError('The id field must be of type UUID')

    name_to_checker = {
        'id': __check_id,
        'account_id': __check_id,
    }

    async def Get(
        self,
        request: profiles_pb2.ProfilesGetRequest,
        context: grpc.aio.ServicerContext
    ) -> profiles_pb2.ProfilesGetResponse:
        identifier_field = request.WhichOneof('identifier')
        if not identifier_field:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                'The id or telegram_id field must be present',
            )
        try:
            await self.name_to_checker[identifier_field](getattr(request, identifier_field))
        except ValueError as exception:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exception))
        specification = EqualsSpecification(identifier_field, getattr(request, identifier_field))
        async with database.pool.acquire() as connection:
            profiles = (await ProfilesRepository.get(connection, specification))