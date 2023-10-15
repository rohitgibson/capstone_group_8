from enum import Enum
from typing import Union

from pydantic import BaseModel

from models.api.searchModels import SearchAddress, SearchResults
from models.api.modifyModels import AddAddress, UpdateAddress, DeleteAddress

class RequestTypes(str, Enum):
    add = "add"
    search = "search"
    update = "update"
    delete = "delete"

class RequestResponse(BaseModel):
    requestType: RequestTypes
    requestData: Union[AddAddress, UpdateAddress, DeleteAddress, SearchAddress, dict]
    requestSuccess: bool
    responseStatusMsg: str
    responseData: Union[SearchResults, dict]