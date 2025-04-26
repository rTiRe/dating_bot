from elasticsearch import AsyncElasticsearch

from config import settings


class DBConnection:
    def __init__(self, host: str, user: str, password: str) -> None:
        self._credentials = {
            'hosts': host,
            'basic_auth': (user, password),
            'verify_certs': False,
        }

    async def __ensure_index_exists(self) -> None:
        if await self.elasticsearch.indices.exists(index='profiles'):
            return
        await self.elasticsearch.indices.create(
            index='profiles',
            body={
                'mappings': {
                    'properties': {
                        'profile_id': {'type': 'keyword'},
                        'location': {'type': 'geo_point'},
                        'age': {'type': 'integer'},
                        'gender': {'type': 'integer'},
                    }
                }
            }
        )

    async def connect(self) -> None:
        self.elasticsearch = AsyncElasticsearch(**self._credentials)
        await self.__ensure_index_exists()


database = DBConnection(
    settings.ELASTICSEARCH_URL,
    settings.ELASTICSEARCH_USER,
    settings.ELASTICSEARCH_PASS.get_secret_value(),
)
