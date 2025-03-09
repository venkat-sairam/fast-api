from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Role(str, Enum):
    teacher = "teacher"
    student = "student"


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    email: str = Field(max_length=100, unique=True, index=True, nullable=False)
    role: Role = Field(default=Role.student)
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": "now()"},
        nullable=False,
        default_factory=lambda: datetime.now(timezone.utc),
    )
    is_active: bool = Field(default=False)
    password_hash: str = Field(exclude=True)
    # Relationship to Profile (one-to-one)
    profile: Optional["Profile"] = Relationship(back_populates="owner", sa_relationship_kwargs={"uselist": False})


class Profile(SQLModel, table=True):
    __tablename__ = "profiles"
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=100, nullable=False)
    last_name: str = Field(max_length=100, nullable=False)
    bio: Optional[str] = Field(default=None)
    is_active: bool = Field(default=False)
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": "now()"},
        nullable=False,
        default_factory=lambda: datetime.now(timezone.utc),
    )
    user_id: int = Field(foreign_key="users.id", nullable=False)

    # Relationship to User (one-to-one)
    owner: Optional[User] = Relationship(back_populates="profile")
