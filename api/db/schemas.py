from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

#  Structure of the request from the user.
#  This is the schema that we will use to validate the request that we will receive from the user.


class User_request(SQLModel):
    name: str
    email: str
    role: str
    password: str = Field(..., min_length=8)


class User_login_response(SQLModel):
    token: str
    token_type: str


class User_login(SQLModel):
    email: str
    password: str = Field(..., min_length=8)


# Structure of the response to the user.
#  In other words, this is the schema of the response that we will send to the user.
#  This is the schema that we will use to validate the response that we will send to the user.
class User_response(SQLModel):
    id: Optional[int] = None
    name: str
    email: str
    role: str
    created_at: Optional[datetime] = None
