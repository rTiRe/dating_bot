from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

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
    __slots__ = ("account_id", "first_name", "last_name", "age", "gender", "biography", "additional_info", "language_locale")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    BIOGRAPHY_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_INFO_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_LOCALE_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    first_name: str
    last_name: str
    age: int
    gender: Gender
    biography: str
    additional_info: str
    language_locale: str
    def __init__(self, account_id: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., age: _Optional[int] = ..., gender: _Optional[_Union[Gender, str]] = ..., biography: _Optional[str] = ..., additional_info: _Optional[str] = ..., language_locale: _Optional[str] = ...) -> None: ...

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
        __slots__ = ("account_id", "first_name", "last_name", "age", "gender", "biography", "additional_info", "language_locale")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
        LAST_NAME_FIELD_NUMBER: _ClassVar[int]
        AGE_FIELD_NUMBER: _ClassVar[int]
        GENDER_FIELD_NUMBER: _ClassVar[int]
        BIOGRAPHY_FIELD_NUMBER: _ClassVar[int]
        ADDITIONAL_INFO_FIELD_NUMBER: _ClassVar[int]
        LANGUAGE_LOCALE_FIELD_NUMBER: _ClassVar[int]
        account_id: str
        first_name: str
        last_name: str
        age: int
        gender: Gender
        biography: str
        additional_info: str
        language_locale: str
        def __init__(self, account_id: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., age: _Optional[int] = ..., gender: _Optional[_Union[Gender, str]] = ..., biography: _Optional[str] = ..., additional_info: _Optional[str] = ..., language_locale: _Optional[str] = ...) -> None: ...
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
    __slots__ = ("id", "account_id", "first_name", "last_name", "age", "gender", "biography", "additional_info", "language_locale", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    BIOGRAPHY_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_INFO_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_LOCALE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    account_id: str
    first_name: str
    last_name: str
    age: int
    gender: Gender
    biography: str
    additional_info: str
    language_locale: str
    created_at: str
    updated_at: str
    def __init__(self, id: _Optional[str] = ..., account_id: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., age: _Optional[int] = ..., gender: _Optional[_Union[Gender, str]] = ..., biography: _Optional[str] = ..., additional_info: _Optional[str] = ..., language_locale: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...

class ProfilesGetResponse(_message.Message):
    __slots__ = ("id", "account_id", "first_name", "last_name", "age", "gender", "biography", "additional_info", "language_locale", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    BIOGRAPHY_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_INFO_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_LOCALE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    account_id: str
    first_name: str
    last_name: str
    age: int
    gender: Gender
    biography: str
    additional_info: str
    language_locale: str
    created_at: str
    updated_at: str
    def __init__(self, id: _Optional[str] = ..., account_id: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., age: _Optional[int] = ..., gender: _Optional[_Union[Gender, str]] = ..., biography: _Optional[str] = ..., additional_info: _Optional[str] = ..., language_locale: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...

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
