from typing import Union, List, Optional

from pydantic import BaseModel, constr, Field

from models.db.addressModels import CountryEnum, StateEnum, ProvEnum, Address

class SearchQuery(BaseModel):
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
    searchQuery: SearchQuery
    addressVerified: bool
    recommendedAddresses: Optional[List[SearchResult]] = Field(default=None)
