from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AccountsGetRequest(_message.Message):
    __slots__ = ("telegram_id", "telegram_username")
    TELEGRAM_ID_FIELD_NUMBER: _ClassVar[int]
    TELEGRAM_USERNAME_FIELD_NUMBER: _ClassVar[int]
    telegram_id: int
    telegram_username: str
    def __init__(self, telegram_id: _Optional[int] = ..., telegram_username: _Optional[str] = ...) -> None: ...

class AccountsGetResponse(_message.Message):
    __slots__ = ("id", "telegram_id", "telegram_username", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    TELEGRAM_ID_FIELD_NUMBER: _ClassVar[int]
    TELEGRAM_USERNAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    telegram_id: int
    telegram_username: str
    created_at: str
    updated_at: str
    def __init__(self, id: _Optional[str] = ..., telegram_id: _Optional[int] = ..., telegram_username: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...
