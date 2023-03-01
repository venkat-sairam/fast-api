from pydantic import BaseModel, EmailStr
from datetime import datetime


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


class PostResponse(BaseModel):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PostAllResponses(PostBase):

    created_at: datetime

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    email: EmailStr
    password: str
