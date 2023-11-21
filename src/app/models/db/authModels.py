from typing import Optional, Union, Annotated, List
from uuid import uuid4

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped
from pydantic import BaseModel, Field

class Base(DeclarativeBase):
    pass

class Role(Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(20), primary_key=True)

class RoleCheck(BaseModel):
    name: str = Field(max_length=20)

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(128), index=True, nullable=False, unique=True)
    password: Mapped[BLOB] = mapped_column(String(256), index=False, nullable=False, unique=True)
    role: Mapped[str] = mapped_column(ForeignKey("roles.name"))

class UserCheck(BaseModel):
    username: str = Field(max_length=128)
    password: str = Field(max_length=256)
    role: str = Field(max_length=20)