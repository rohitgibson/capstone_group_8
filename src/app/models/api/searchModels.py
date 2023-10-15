from typing import Union, List, Optional

from pydantic import BaseModel, constr, Field, ValidationError, model_validator, ConfigDict

from models.db.addressModels import CountryEnum, StateEnum, ProvEnum, Address

class SearchAddress(BaseModel):
    model_config = ConfigDict(str_to_upper=True, str_strip_whitespace=True)

    address: Address

class SearchResult(BaseModel):
    key: str
    address: Address

class SearchResults(BaseModel):
    addressVerified: bool
    recommendedAddresses: Optional[List[SearchResult]] = Field(default=[])
