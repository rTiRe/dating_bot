from ..profiles import profiles_pb2 as _profiles_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RecommendationsSearchProfilesRequest(_message.Message):
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
    gender: _profiles_pb2.Gender
    age_min: int
    age_max: int
    distance: int
    limit: int
    def __init__(self, lat: _Optional[float] = ..., lon: _Optional[float] = ..., gender: _Optional[_Union[_profiles_pb2.Gender, str]] = ..., age_min: _Optional[int] = ..., age_max: _Optional[int] = ..., distance: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class RecommendationsSearchProfilesResponse(_message.Message):
    __slots__ = ("profile_ids", "total")
    PROFILE_IDS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    profile_ids: _containers.RepeatedScalarFieldContainer[str]
    total: int
    def __init__(self, profile_ids: _Optional[_Iterable[str]] = ..., total: _Optional[int] = ...) -> None: ...

class RecommendationsUpdateProfileRequest(_message.Message):
    __slots__ = ("profile_id", "age", "gender", "city_point", "user_point")
    PROFILE_ID_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    CITY_POINT_FIELD_NUMBER: _ClassVar[int]
    USER_POINT_FIELD_NUMBER: _ClassVar[int]
    profile_id: str
    age: int
    gender: _profiles_pb2.Gender
    city_point: _profiles_pb2.CityPoint
    user_point: _profiles_pb2.UserPoint
    def __init__(self, profile_id: _Optional[str] = ..., age: _Optional[int] = ..., gender: _Optional[_Union[_profiles_pb2.Gender, str]] = ..., city_point: _Optional[_Union[_profiles_pb2.CityPoint, _Mapping]] = ..., user_point: _Optional[_Union[_profiles_pb2.UserPoint, _Mapping]] = ...) -> None: ...

class RecommendationsUpdateProfileResponse(_message.Message):
    __slots__ = ("profile_id", "age", "gender", "city_id", "city_point", "user_point", "result")
    PROFILE_ID_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    CITY_ID_FIELD_NUMBER: _ClassVar[int]
    CITY_POINT_FIELD_NUMBER: _ClassVar[int]
    USER_POINT_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    profile_id: str
    age: int
    gender: _profiles_pb2.Gender
    city_id: str
    city_point: _profiles_pb2.CityPoint
    user_point: _profiles_pb2.UserPoint
    result: str
    def __init__(self, profile_id: _Optional[str] = ..., age: _Optional[int] = ..., gender: _Optional[_Union[_profiles_pb2.Gender, str]] = ..., city_id: _Optional[str] = ..., city_point: _Optional[_Union[_profiles_pb2.CityPoint, _Mapping]] = ..., user_point: _Optional[_Union[_profiles_pb2.UserPoint, _Mapping]] = ..., result: _Optional[str] = ...) -> None: ...

class RecommendationsUpdateCityRequest(_message.Message):
    __slots__ = ("city_id", "lat", "lon")
    CITY_ID_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    city_id: str
    lat: float
    lon: float
    def __init__(self, city_id: _Optional[str] = ..., lat: _Optional[float] = ..., lon: _Optional[float] = ...) -> None: ...

class RecommendationsUpdateCityResponse(_message.Message):
    __slots__ = ("city_id", "lat", "lon", "result")
    CITY_ID_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    city_id: str
    lat: float
    lon: float
    result: str
    def __init__(self, city_id: _Optional[str] = ..., lat: _Optional[float] = ..., lon: _Optional[float] = ..., result: _Optional[str] = ...) -> None: ...

class RecommendationsSearchCitiesRequest(_message.Message):
    __slots__ = ("lat", "lon", "distance", "limit")
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    lat: float
    lon: float
    distance: float
    limit: int
    def __init__(self, lat: _Optional[float] = ..., lon: _Optional[float] = ..., distance: _Optional[float] = ..., limit: _Optional[int] = ...) -> None: ...

class RecommendationsSearchCitiesResponse(_message.Message):
    __slots__ = ("city_ids", "total")
    CITY_IDS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    city_ids: _containers.RepeatedScalarFieldContainer[str]
    total: int
    def __init__(self, city_ids: _Optional[_Iterable[str]] = ..., total: _Optional[int] = ...) -> None: ...
