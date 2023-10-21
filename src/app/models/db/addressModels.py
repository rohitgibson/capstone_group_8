from typing import Optional, Union, Any
from typing_extensions import Annotated
from enum import Enum
from uuid import uuid4

# from redis_om import HashModel, VectorFieldOptions, Field
from pydantic import BaseModel, ValidationError, model_validator, field_validator, constr, Field, InstanceOf, ConfigDict

from models.db.enumModels import CountryEnum, StateEnum, ProvEnum

from utils.modelUtils import CheckPostalCode

checkPostalCode = CheckPostalCode()

class Address(BaseModel):
    model_config = ConfigDict(str_to_upper=True, str_strip_whitespace=True)

    # firstName: str = Field(min_length=1)
    # lastName: str = Field(min_length=1)
    addressLine1: str 
    addressLine2: Optional[str] = Field(default="")
    city: str 
    stateProv: Union[StateEnum, ProvEnum] 
    postalCode: str 
    country: CountryEnum 

    # Checks that stateProv enum is compatible with country enum 
    @model_validator(mode='after')
    def check_stateProv_valid(self) -> 'Address':
        stateProv = self.stateProv
        country = self.country
        postalCode = self.postalCode

        if country == "US" and type(stateProv) == StateEnum or country == "CA" and type(stateProv) == ProvEnum:
            postalCodeValid:bool = checkPostalCode.postalCodeVerification(stateProv=stateProv, postalCode=postalCode)

            if postalCodeValid is True:
                return self
            else:
                raise ValueError(f'postalCode "{postalCode}" incompatible with stateProv value "{stateProv}" and country value "{country}"')
            
        else:
            raise ValueError(f'stateProv value "{stateProv}" incompatible with country value "{country}"')