from datetime import datetime

from pydantic import BaseModel
import typing as t


class UserBase(BaseModel):
    email: str
    is_active: bool = True
    first_name: str
    last_name: str


class UserOut(UserBase):
    pass


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserEdit(UserBase):
    password: t.Optional[str] = None

    class Config:
        orm_mode = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    permissions: str = "user"


class Message(BaseModel):
    id: int
    from_id: t.Optional[int]
    chat_id: int         # идентификатор в каком диалоге находится
    from_name: str       # кто написал это сообщение
    to_name: str         # кому написали это сообщение
    to_addr_id: str      # id кому написали
    letter: str
    data: datetime
    mark_as_read: bool
    is_your_message: bool


class ConversationDialog(BaseModel):
    # chat_id: int
    messages: t.List[Message]


class ResponseLetter(BaseModel):
    status: bool
    delay: int
    chat_id: int


class Friend(BaseModel):
    id: int
    full_name: str
    category: t.List[str]


class UserFriend(Friend):
    friends: t.List[str]
    friendship_in: t.List[int]
    friendship_out: t.List[int]
