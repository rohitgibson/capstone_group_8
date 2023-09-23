from typing import Optional, Union, Annotated

from pydantic import BaseModel, SecretStr

class User(BaseModel):
    username: str
    password: SecretStr