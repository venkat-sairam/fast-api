from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class Post(BaseModel):  # Schema of the Request body

    title: str
    content: str
    published: bool = True


class PostBase(BaseModel):

    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):

    id: int
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PostAllResponses(PostBase):
    id: str
    owner_id: str
    created_at: datetime

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class ResponseToUser(BaseModel):
    id: Optional[int]
    email: Optional[EmailStr]
    created_at: Optional[datetime]
    message: Optional[str]

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]
