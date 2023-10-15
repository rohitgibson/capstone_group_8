from typing import Union, List, Optional

from pydantic import BaseModel, constr, Field, ValidationError, model_validator, ConfigDict

from models.db.addressModels import CountryEnum, StateEnum, ProvEnum, Address

class SearchRequest(BaseModel):
    model_config = ConfigDict(str_to_upper=True, str_strip_whitespace=True)

    data: Address

class SearchResult(BaseModel):
    key: str
    data: Address

class SearchResults(BaseModel):
    searchRequest: Address
    addressVerified: bool
    recommendedAddresses: Optional[List[SearchResult]] = Field(default=None)
