from typing import Union

from pydantic import BaseModel, constr

from models.api.addModels import CountryEnum, StateEnum, ProvEnum, Address

class SearchQuery(BaseModel):
    addressLine1: str
    addressLine2: str 
    city: str 
    stateProv: Union[StateEnum, ProvEnum]
    postalCode: str
    country: CountryEnum

