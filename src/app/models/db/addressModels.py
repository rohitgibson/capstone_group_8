from typing import Optional, Union, Any
from re import fullmatch

# from redis_om import HashModel, VectorFieldOptions, Field
from pydantic import BaseModel, ValidationError, model_validator, field_validator, constr, Field, InstanceOf, ConfigDict

from models.db.enumModels import CountryEnum, StateEnum, ProvEnum

from utils.modelUtils import CheckPostalCode

checkPostalCode = CheckPostalCode()

class Address(BaseModel):
    """
    A Pydantic model that represents an address.    
    """
    model_config = ConfigDict(str_to_upper=True, str_strip_whitespace=True)

    addressLine1: str 
    addressLine2: Optional[str] = Field(default="")
    city: str 
    stateProv: Union[StateEnum, ProvEnum] 
    postalCode: str 
    country: CountryEnum 

    @model_validator(mode='after')
    def check_stateProv_valid(self) -> 'Address':
        """
        A model validator to check that the `stateProv` and 
        `postalCode` fields are compatible with the 
        `country` field.

        Args:
            `self`: 
                The `Address` object.

        Returns:
            The `Address` object if the `stateProv` and 
            `postalCode` fields are compatible with the `country`
            field. Otherwise, raises a `ValueError` exception.
        """
        stateProv = self.stateProv
        country = self.country
        postalCode = self.postalCode

        # Check if the `country` field is equal to "US" and 
        # the `stateProv` field is of type `StateEnum`, or if
        # the `country` field is equal to "CA" and the `stateProv`
        # field is of type `ProvEnum`.
        if country == "US" and type(stateProv) == StateEnum and fullmatch(checkPostalCode.postalCodeRegexUS, postalCode) is not None or country == "CA" and type(stateProv) == ProvEnum and fullmatch(checkPostalCode.postalCodeRegexCA, postalCode) is not None:
            # Call the `checkPostalCode.postalCodeVerification()`
            # function to verify that the `postalCode` field is
            # valid for the given `stateProv` field

            if checkPostalCode.postalCodeVerification(country=country, stateProv=stateProv, postalCode=postalCode) is True:
                # If the `postalCode` field is valid, return the
                # `Address` object.
                return self
            else:
                # If the `postalCode` field is not valid, 
                # raise a `ValueError` exception.
                raise ValueError(f'postalCode "{postalCode}" incompatible with stateProv value "{stateProv}" and country value "{country}"')
            
        else:
            # If the `country` and `stateProv` fields are
            # not compatible, raise a `ValueError` exception.
            raise ValueError(f'stateProv value "{stateProv}" and/or postalCode "{postalCode}" value is incompatible with country value "{country}"')