from src.storage.elasticsearch import database

async def search_profiles(
    point: dict[str, float],
    age: int,
    gender: int,
    distance: int = 25,
    prefer: str = 'city',
    limit: int = 10,
) -> tuple[list[str], int]:
    gender_must = []
    if gender == 1:
        gender_must = [{'term': {'gender': 1}}]
    elif gender == 2:
        gender_must = [{'term': {'gender': 2}}]
    if prefer == 'city':
        main_point_field = 'city_point'
        secondary_point_field = 'user_point'
    else:
        main_point_field = 'user_point'
        secondary_point_field = 'city_point'
    query = {
        'query': {
            'function_score': {
                'query': {
                    'bool': {
                        'must': [
                            {'range': {'age': {'gte': age-2, 'lte': age+2}}},
                            *gender_must,
                        ],
                        'filter': [{'bool': {
                            'should': [
                                {'geo_distance': {
                                    'distance': f'{distance}km',
                                    main_point_field: point,
                                }},
                                {'geo_distance': {
                                    'distance': f'{distance}km',
                                    secondary_point_field: point,
                                }},
                            ],
                            'minimum_should_match': 1,
                        }}],
                    }
                },
                'functions': [
                    {
                        'filter': {
                            'exists': {
                                'field': main_point_field,
                            }
                        },
                        'gauss': {
                            main_point_field: {
                                'origin': point,
                                'scale': f'{distance / 2.2}km',
                                'offset': '500m',
                                'decay': 0.5,
                            },
                        },
                        'weight': 55 if prefer == 'user' else 100,
                    },
                    {
                        'filter': {
                            'exists': {
                                'field': secondary_point_field,
                            }
                        },
                        'gauss': {
                            secondary_point_field: {
                                'origin': point,
                                'scale': f'{distance / 2.2}km',
                                'offset': '500m',
                                'decay': 0.5,
                            },
                        },
                        'weight': 45 if prefer == 'user' else 0,
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
                            'field': 'rating',
                            'factor': 1.0,
                            'modifier': 'none',
                        },
                        'weight': 1,
                    },
                    {
                        'random_score': {},
                        'weight': 30,
                    },
                ],
                'score_mode': 'sum',
                'boost_mode': 'multiply',
            }
        }
    }
    search_response = await database.elasticsearch.search(
        index='profiles',
        body=query,
        size=limit,
    )
    hits = search_response['hits']['hits']
    print(hits, flush=True)
    return [hit['_id'] for hit in hits], search_response['hits']['total']['value']
