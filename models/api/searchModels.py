from typing import Union, List, Optional

from pydantic import BaseModel, constr, Field

from models.db.addressModels import CountryEnum, StateEnum, ProvEnum, Address

class SearchQuery(BaseModel):
    addressLine1: str = Field(constr(strip_whitespace=True))
    addressLine2: str = Field(constr(strip_whitespace=True))
    city: str = Field(constr(strip_whitespace=True))
    stateProv: Union[StateEnum, ProvEnum] = Field(constr(strip_whitespace=True, to_upper=True))
    postalCode: str = Field(constr(strip_whitespace=True, to_upper=True))
    country: CountryEnum = Field(constr(strip_whitespace=True))

class SearchResult(BaseModel):
    key: str
    data: Address

class SearchResults(BaseModel):
    searchQuery: SearchQuery
    addressVerified: bool
    recommendedAddresses: Optional[List[SearchResult]] = Field(default=None)
