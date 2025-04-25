from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Gender(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GENDER_DEFAULT: _ClassVar[Gender]
    GENDER_MALE: _ClassVar[Gender]
    GENDER_FEMALE: _ClassVar[Gender]
GENDER_DEFAULT: Gender
GENDER_MALE: Gender
GENDER_FEMALE: Gender

class ProfileCreateRequest(_message.Message):
    __slots__ = ("account_id", "name", "age", "gender", "biography", "language_locale", "image_base64_list", "lat", "lon", "interested_in")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    BIOGRAPHY_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_LOCALE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_BASE64_LIST_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    INTERESTED_IN_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    name: str
    age: int
    gender: Gender
    biography: str
    language_locale: str
    image_base64_list: _containers.RepeatedScalarFieldContainer[str]
    lat: float
    lon: float
    interested_in: Gender
    def __init__(self, account_id: _Optional[str] = ..., name: _Optional[str] = ..., age: _Optional[int] = ..., gender: _Optional[_Union[Gender, str]] = ..., biography: _Optional[str] = ..., language_locale: _Optional[str] = ..., image_base64_list: _Optional[_Iterable[str]] = ..., lat: _Optional[float] = ..., lon: _Optional[float] = ..., interested_in: _Optional[_Union[Gender, str]] = ...) -> None: ...

class ProfilesGetRequest(_message.Message):
    __slots__ = ("id", "account_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    account_id: str
    def __init__(self, id: _Optional[str] = ..., account_id: _Optional[str] = ...) -> None: ...

class ProfileUpdateRequest(_message.Message):
    __slots__ = ("id", "data")
    class UpdateData(_message.Message):
        __slots__ = ("account_id", "name", "age", "gender", "biography", "language_locale", "image_base64_list", "lat", "lon", "interested_in")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        AGE_FIELD_NUMBER: _ClassVar[int]
        GENDER_FIELD_NUMBER: _ClassVar[int]
        BIOGRAPHY_FIELD_NUMBER: _ClassVar[int]
        LANGUAGE_LOCALE_FIELD_NUMBER: _ClassVar[int]
        IMAGE_BASE64_LIST_FIELD_NUMBER: _ClassVar[int]
        LAT_FIELD_NUMBER: _ClassVar[int]
        LON_FIELD_NUMBER: _ClassVar[int]
        INTERESTED_IN_FIELD_NUMBER: _ClassVar[int]
        account_id: str
        name: str
        age: int
        gender: Gender
        biography: str
        language_locale: str
        image_base64_list: _containers.RepeatedScalarFieldContainer[str]
        lat: float
        lon: float
        interested_in: Gender
        def __init__(self, account_id: _Optional[str] = ..., name: _Optional[str] = ..., age: _Optional[int] = ..., gender: _Optional[_Union[Gender, str]] = ..., biography: _Optional[str] = ..., language_locale: _Optional[str] = ..., image_base64_list: _Optional[_Iterable[str]] = ..., lat: _Optional[float] = ..., lon: _Optional[float] = ..., interested_in: _Optional[_Union[Gender, str]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    data: ProfileUpdateRequest.UpdateData
    def __init__(self, id: _Optional[str] = ..., data: _Optional[_Union[ProfileUpdateRequest.UpdateData, _Mapping]] = ...) -> None: ...

class ProfileDeleteRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ProfileCreateResponse(_message.Message):
    __slots__ = ("id", "account_id", "name", "age", "gender", "biography", "language_locale", "created_at", "updated_at", "image_base64_list", "lat", "lon", "rating", "interested_in")
    ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    BIOGRAPHY_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_LOCALE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    IMAGE_BASE64_LIST_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    INTERESTED_IN_FIELD_NUMBER: _ClassVar[int]
    id: str
    account_id: str
    name: str
    age: int
    gender: Gender
    biography: str
    language_locale: str
    created_at: str
    updated_at: str
    image_base64_list: _containers.RepeatedScalarFieldContainer[str]
    lat: float
    lon: float
    rating: int
    interested_in: Gender
    def __init__(self, id: _Optional[str] = ..., account_id: _Optional[str] = ..., name: _Optional[str] = ..., age: _Optional[int] = ..., gender: _Optional[_Union[Gender, str]] = ..., biography: _Optional[str] = ..., language_locale: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., image_base64_list: _Optional[_Iterable[str]] = ..., lat: _Optional[float] = ..., lon: _Optional[float] = ..., rating: _Optional[int] = ..., interested_in: _Optional[_Union[Gender, str]] = ...) -> None: ...

class ProfilesGetResponse(_message.Message):
    __slots__ = ("id", "account_id", "name", "age", "gender", "biography", "language_locale", "created_at", "updated_at", "image_base64_list", "lat", "lon", "rating", "interested_in")
    ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    BIOGRAPHY_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_LOCALE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    IMAGE_BASE64_LIST_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    INTERESTED_IN_FIELD_NUMBER: _ClassVar[int]
    id: str
    account_id: str
    name: str
    age: int
    gender: Gender
    biography: str
    language_locale: str
    created_at: str
    updated_at: str
    image_base64_list: _containers.RepeatedScalarFieldContainer[str]
    lat: float
    lon: float
    rating: int
    interested_in: Gender
    def __init__(self, id: _Optional[str] = ..., account_id: _Optional[str] = ..., name: _Optional[str] = ..., age: _Optional[int] = ..., gender: _Optional[_Union[Gender, str]] = ..., biography: _Optional[str] = ..., language_locale: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., image_base64_list: _Optional[_Iterable[str]] = ..., lat: _Optional[float] = ..., lon: _Optional[float] = ..., rating: _Optional[int] = ..., interested_in: _Optional[_Union[Gender, str]] = ...) -> None: ...

class ProfilesUpdateResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: str
    def __init__(self, result: _Optional[str] = ...) -> None: ...

class ProfilesDeleteResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: str
    def __init__(self, result: _Optional[str] = ...) -> None: ...
