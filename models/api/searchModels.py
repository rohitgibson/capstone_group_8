from typing import Union, List

from pydantic import BaseModel, constr

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
    results: List[SearchResult]
