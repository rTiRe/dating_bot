from src.storage.elasticsearch import database

async def search_cities(
    lat: float,
    lon: float,
    distance: float,
    limit: int,
) -> tuple[list[tuple[str, dict[str, float]]], int]:
    query = {
        'bool': {
            'must': {
                'match_all': {},
            },
            'filter': {
                'geo_distance': {
                    'distance': f'{distance}km',
                    'point': {'lat': lat, 'lon': lon},
                },
            },
        },
    }
    sort = {
        '_geo_distance': {
            'point': {'lat': lat, 'lon': lon},
            'order': 'asc',
            'unit': 'km',
            'distance_type': 'plane',
        },
    }
    response = await database.elasticsearch.search(
        index='cities',
        query=query,
        size=limit,
        sort=sort,
    )
    hits = response['hits']['hits']
    city_ids = []
    total = response['hits']['total']['value']
    for hit in hits:
        city_ids.append((hit['_id'], hit['_source']['point']))
    return city_ids, total