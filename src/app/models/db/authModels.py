from typing import Optional, Union, Annotated, List
from uuid import uuid4

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped

class Base(DeclarativeBase):
    pass

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), index=True, nullable=False, unique=True)


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), index=True, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(256), index=False, nullable=False, unique=True)
    role: Mapped[str] = mapped_column(ForeignKey("roles.id"))


    # id: Optional[str] = Field(default_factory=lambda: str(uuid4()))
    # name: str
    # password: SecretBytes
    # role: str = Field(alias="role.name")


    