"""Package for manage GRPC connections."""

from src.api.grpc.connections.accounts import AccountsConnection, accounts_connection
from src.api.grpc.connections.base import BaseConnection

__all__ = [
    'accounts_connection',
]
