from prometheus_client import Counter, Histogram

GRPC_REQUEST_COUNT = Counter(
    'profiles_service_requests_total',
    'Total number of gRPC requests processed',
    ['method', 'status_code']
)
GRPC_REQUEST_LATENCY = Histogram(
    'profiles_service_request_duration_seconds',
    'Latency of gRPC requests in seconds',
    ['method']
)