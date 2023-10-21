from typing import Optional, Union, Any
from enum import Enum
from uuid import uuid4, UUID

# from redis_om import HashModel, VectorFieldOptions, Field
from pydantic import BaseModel, ValidationError, field_validator, constr, Field, ConfigDict

from models.db.addressModels import Address
from models.api.searchModels import SearchAddress, SearchResults

class AddAddress(BaseModel):
    model_config = ConfigDict(str_to_upper=True, str_strip_whitespace=True)

    address: Union[Address, list[Address]]

class UpdateAddress(BaseModel):
    key: str    
    address: Address

    @field_validator('key')
    @classmethod
    def check_key_format(cls, v: str) -> str:
        v_split = v.split(':')
        if v_split[0] == "address":
            return v
        else:
            raise ValueError("Key in incorrect format. Must begin with 'address.'")

class DeleteAddress(BaseModel):
    key: str

    @field_validator('key')
    @classmethod
    def check_key_format(cls, v: str) -> str:
        v_split = v.split(':')
        if v_split[0] == "address":
            return v
        else:
            raise ValueError("Key in incorrect format. Must begin with 'address.'")
        
