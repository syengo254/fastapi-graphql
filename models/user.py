from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    __tablename__: str = "users"

    id: Optional[int] = Field(None, primary_key=True, nullable=False)
    email: str = Field(unique=True, index=True)
    name: str = Field(max_length=60)
    password: str
