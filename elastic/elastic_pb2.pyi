from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetMatchRequest(_message.Message):
    __slots__ = ("lat", "lon", "gender", "age_min", "age_max", "distance", "limit")
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    AGE_MIN_FIELD_NUMBER: _ClassVar[int]
    AGE_MAX_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    lat: float
    lon: float
    gender: str
    age_min: int
    age_max: int
    distance: int
    limit: int
    def __init__(self, lat: _Optional[float] = ..., lon: _Optional[float] = ..., gender: _Optional[str] = ..., age_min: _Optional[int] = ..., age_max: _Optional[int] = ..., distance: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class GetMatchResponse(_message.Message):
    __slots__ = ("user_ids", "total")
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    total: int
    def __init__(self, user_ids: _Optional[_Iterable[str]] = ..., total: _Optional[int] = ...) -> None: ...

class UpdateUserRequest(_message.Message):
    __slots__ = ("user_id", "lat", "lon", "age", "gender")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    lat: float
    lon: float
    age: int
    gender: str
    def __init__(self, user_id: _Optional[str] = ..., lat: _Optional[float] = ..., lon: _Optional[float] = ..., age: _Optional[int] = ..., gender: _Optional[str] = ...) -> None: ...

class UpdateUserResponse(_message.Message):
    __slots__ = ("user_id", "created")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    created: bool
    def __init__(self, user_id: _Optional[str] = ..., created: bool = ...) -> None: ...
