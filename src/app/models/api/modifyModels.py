from typing import Optional, Union, Any
from enum import Enum
from uuid import uuid4

# from redis_om import HashModel, VectorFieldOptions, Field
from pydantic import BaseModel, ValidationError, field_validator, constr, Field

from models.db.addressModels import Address
from models.api.searchModels import SearchResults

class AddAddress(BaseModel):
    data: Address

class UpdateAddress(BaseModel):
    key: str    
    data: Address

class DeleteAddress(BaseModel):
    key: str

class RequestTypes(str, Enum):
    add = "add"
    search = "search"
    modify = "modify"
    delete = "delete"

class RequestResponse(BaseModel):
    requestType: RequestTypes
    requestData: Union[AddAddress, UpdateAddress, DeleteAddress, SearchResults, dict]
    requestSuccess: bool
    responseMsg: str