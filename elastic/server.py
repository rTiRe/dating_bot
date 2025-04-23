from elasticsearch import Elasticsearch
import grpc
from concurrent import futures
import elastic_pb2
import elastic_pb2_grpc
import math
from typing import List, Tuple
import os
class ElasticSearchServicer(elastic_pb2_grpc.ElasticSearchServicer):
    def __init__(self):
        print(os.getenv('ELASTICSEARCH_URL', 'http://localhost:9200'),)
        self.es = Elasticsearch(
            os.getenv('ELASTICSEARCH_URL', 'http://localhost:9200'),
            basic_auth=('elastic', 'changeme'),
            verify_certs=False
        )
        self._ensure_index_exists()

    def _ensure_index_exists(self):
        """Ensure the users index exists with proper mappings"""
        if not self.es.indices.exists(index="users"):
            self.es.indices.create(
                index="users",
                body={
                    "mappings": {
                        "properties": {
                            "user_id": {"type": "keyword"},
                            "location": {"type": "geo_point"},
                            "age": {"type": "integer"},
                            "gender": {"type": "keyword"},
                            "created_at": {"type": "date"}
                        }
                    }
                }
            )

    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points using Haversine formula"""
        R = 6371  # Earth's radius in kilometers

        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        return R * c

    def GetMatch(self, request, context):
        """Get matches based on location, gender, and age criteria"""
        try:
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {"term": {"gender": request.gender}},
                            {"range": {"age": {"gte": request.age_min, "lte": request.age_max}}}
                        ],
                        "filter": {
                            "geo_distance": {
                                "distance": f"{request.distance}km",
                                "location": {
                                    "lat": request.lat,
                                    "lon": request.lon
                                }
                            }
                        }
                    }
                },
                "size": request.limit
            }

            response = self.es.search(index="users", body=query)
            hits = response["hits"]["hits"]

            user_ids = [hit["_source"]["user_id"] for hit in hits]
            total = response["hits"]["total"]["value"]

            return elastic_pb2.GetMatchResponse(
                user_ids=user_ids,
                total=total
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return elastic_pb2.GetMatchResponse()

    def UpdateUser(self, request, context):
        """Update or create a user document"""
        try:
            doc = {
                "user_id": request.user_id,
                "location": {
                    "lat": request.lat,
                    "lon": request.lon
                },
                "age": request.age,
                "gender": request.gender
            }

            response = self.es.index(
                index="users",
                id=request.user_id,
                body=doc,
                op_type="index"
            )

            created = response["result"] == "created"
            return elastic_pb2.UpdateUserResponse(
                user_id=request.user_id,
                created=created
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return elastic_pb2.UpdateUserResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    elastic_pb2_grpc.add_ElasticSearchServicer_to_server(
        ElasticSearchServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
