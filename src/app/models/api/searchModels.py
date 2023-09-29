from typing import Union, List, Optional

from pydantic import BaseModel, constr, Field, ValidationError, model_validator, ConfigDict

from models.db.addressModels import CountryEnum, StateEnum, ProvEnum, Address

class SearchQuery(BaseModel):
    model_config = ConfigDict(str_to_upper=True, str_strip_whitespace=True)

    addressLine1: str
    addressLine2: str
    city: str 
    stateProv: Union[StateEnum, ProvEnum] 
    postalCode: str 
    country: CountryEnum 

class SearchResult(BaseModel):
    key: str
    data: Address

class SearchResults(BaseModel):
    searchRequest: SearchQuery
    addressVerified: bool
    recommendedAddresses: Optional[List[SearchResult]] = Field(default=None)
