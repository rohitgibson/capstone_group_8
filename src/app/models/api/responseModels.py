from enum import Enum
from typing import Union
from datetime import datetime 

from pydantic import BaseModel

from models.api.searchModels import SearchAddress, SearchResults
from models.api.modifyModels import AddAddress, UpdateAddress, DeleteAddress
from models.db.authModels import UserCheck, UserUpdate, UserDelete

class RequestTypes(str, Enum):
    add_address = "add_address"
    search_address = "search_address"
    update_address = "update_address"
    delete_address = "delete_address"
    add_user = "add_user"
    update_user = "update_user"
    delete_user = "delete_user"
    demo_resetdb = "demo_resetdb"


class RequestResponse(BaseModel):
    requestType: RequestTypes
    requestData: Union[AddAddress, 
                       UpdateAddress, 
                       DeleteAddress, 
                       SearchAddress, 
                       UserCheck,
                       UserUpdate,
                       UserDelete,
                       dict]
    requestSuccess: bool
    responseTimestamp: datetime
    responseStatusMsg: str
    responseData: Union[SearchResults, dict]




