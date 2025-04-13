from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Gender(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GENDER_MALE: _ClassVar[Gender]
    GENDER_FEMALE: _ClassVar[Gender]
GENDER_MALE: Gender
GENDER_FEMALE: Gender

class ProfilesGetRequest(_message.Message):
    __slots__ = ("id", "account_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    account_id: str
    def __init__(self, id: _Optional[str] = ..., account_id: _Optional[str] = ...) -> None: ...

class ProfilesGetResponse(_message.Message):
    __slots__ = ("id", "account_id", "first_name", "last_name", "age", "gender", "biography", "additional_info")
    ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    BIOGRAPHY_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_INFO_FIELD_NUMBER: _ClassVar[int]
    id: str
    account_id: str
    first_name: str
    last_name: str
    age: int
    gender: Gender
    biography: str
    additional_info: str
    def __init__(self, id: _Optional[str] = ..., account_id: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., age: _Optional[int] = ..., gender: _Optional[_Union[Gender, str]] = ..., biography: _Optional[str] = ..., additional_info: _Optional[str] = ...) -> None: ...
