"""Package for manage GRPC connections."""

from src.api.grpc.connections.accounts import AccountsConnection, accounts_connection
from src.api.grpc.connections.profiles import ProfilesConnection, profiles_connection
from src.api.grpc.connections.recommendations import RecommendationsConnection, recommendations_connection
from src.api.grpc.connections.clickhoues import ClickhouseConnection, interactions_connection
from src.api.grpc.connections.base import BaseConnection

__all__ = [
    'accounts_connection',
    'profiles_connection',
    'recommendations_connection',
    'interactions_connection',
]
