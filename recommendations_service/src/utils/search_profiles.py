from src.storage.elasticsearch import database

async def search_profiles(
    city_point: dict[str, float],
    age: int,
    gender: int,
    radius_km: int = 25,
) -> tuple[list[str], int]:
    gender_must = []
    if gender == 1:
        gender_must = [{'term': {'gender': 1}}]
    elif gender == 2:
        gender_must = [{'term': {'gender': 2}}]
    query = {
        'query': {
            'function_score': {
                'query': {
                    'bool': {
                        'must': [
                            {'range': {'age': {'gte': age-2, 'lte': age+2}}},
                            *gender_must,
                        ],
                        'filter': [{'geo_distance': {
                            'distance': f'{radius_km}km',
                            'city_point': city_point,
                        }}],
                    }
                },
                'functions': [
                    {
                        'gauss': {
                            'city_point': {
                                'origin': city_point,
                                'scale': f'{radius_km / 2.2}km',
                                'offset': '500m',
                                'decay': 0.5,
                            },
                        },
                        'weight': 100,
                    },
                    {
                        'gauss': {
                            'age': {
                                'origin': age,
                                'scale': 1.0,
                                'offset': 0,
                                'decay': 0.5,
                            },
                        },
                        'weight': 20,
                    },
                    {
                        'field_value_factor': {
                            'field': 'points',
                            'factor': 0.1,
                            'modifier': 'sqrt',
                            'missing': 0,
                        },
                        'weight': 1,
                    },
                    # {
                    #     'random_score': {},
                    #     'weight': 20,
                    # },
                ],
                'score_mode': 'sum',
                'boost_mode': 'multiply',
            }
        }
    }
    search_response = await database.elasticsearch.search(
        index='profiles',
        body=query,
        size=100
    )
    hits = search_response['hits']['hits']
    print(hits, flush=True)
    return [hit['_id'] for hit in hits], search_response['hits']['total']['value']
