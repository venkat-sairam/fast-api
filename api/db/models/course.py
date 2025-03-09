from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class Course(SQLModel, table=True):
    __tablename__ = "courses"
    id: Optional[int] = Field(default=None, primary_key=True)
    courseName: str = Field(max_length=100, nullable=False)
    description: Optional[str] = Field(default=None)
    created_at: str = Field(
        nullable=False, sa_column_kwargs={"server_default": "now()"}, default_factory=lambda: datetime.now(timezone.utc)
    )
