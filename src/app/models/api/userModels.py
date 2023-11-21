from pydantic import BaseModel, Field

class UserCheck(BaseModel):
    username: str = Field(max_length=128)
    password: str = Field(max_length=256)
    role: str = Field(max_length=20)

class Update(BaseModel):
    username: str = Field(max_length=128)
    changes: UserCheck

class Delete(BaseModel):
    username: str = Field(max_length=128)