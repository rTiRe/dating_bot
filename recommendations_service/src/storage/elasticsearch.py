from types import MappingProxyType

from elasticsearch import AsyncElasticsearch

from config import settings


class DBConnection:
    settings = {
        'index': {
            'number_of_shards': 3,
            'number_of_replicas': 2,
        },
    }

    def __init__(self, host: str, user: str, password: str) -> None:
        self._credentials = {
            'hosts': host,
            'basic_auth': (user, password),
            'verify_certs': False,
        }

    async def __ensure_profiles_index_exists(self) -> None:
        # await self.elasticsearch.indices.delete(index='profiles', ignore_unavailable=True)
        if await self.elasticsearch.indices.exists(index='profiles'):
            return
        await self.elasticsearch.indices.create(
            index='profiles',
            mappings={
                'dynamic': False,
                'properties': {
                    'user_point': {'type': 'geo_point'},
                    'city_point': {'type': 'geo_point'},
                    'age': {'type': 'integer'},
                    'gender': {'type': 'integer'},
                    'rating': {'type': 'integer'},
                },
            },
            settings=self.settings,
        )

    async def __ensure_cities_index_exists(self) -> None:
        if await self.elasticsearch.indices.exists(index='cities'):
            return
        await self.elasticsearch.indices.create(
            index='cities',
            mappings={
                'dynamic': False,
                'properties': {
                    'point': {'type': 'geo_point'},
                },
            },
            settings=self.settings,
        )

    async def connect(self) -> None:
        self.elasticsearch = AsyncElasticsearch(**self._credentials)
        await self.__ensure_profiles_index_exists()
        await self.__ensure_cities_index_exists()


database = DBConnection(
    settings.ELASTICSEARCH_URL,
    settings.ELASTICSEARCH_USER,
    settings.ELASTICSEARCH_PASS.get_secret_value(),
)
