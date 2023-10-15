from typing import Optional, Union, Any
from typing_extensions import Annotated
from enum import Enum
from uuid import uuid4

# from redis_om import HashModel, VectorFieldOptions, Field
from pydantic import BaseModel, ValidationError, model_validator, field_validator, constr, Field, InstanceOf, ConfigDict

class CountryEnum(str, Enum):
    US = "US"
    CA = "CA"

# Source: https://www12.statcan.gc.ca/census-recensement/2021/ref/dict/tab/index-eng.cfm?ID=t1_8
class ProvEnum(str, Enum):
    NL = "NL"
    PE = "PE"
    NS = "NS"
    NB = "NB"
    QC = "QC"
    ON = "ON"
    MB = "MB"
    SK = "SK"
    AB = "AB"
    BC = "BC"
    YT = "YT"
    NT = "NT"
    NU = "NU"

# Source: https://www.bls.gov/respondents/mwr/electronic-data-interchange/appendix-d-usps-state-abbreviations-and-fips-codes.htm
class StateEnum(str, Enum):
    AL = "AL"
    AK = "AK"
    AZ = "AZ"
    AR = "AR"
    CA = "CA"
    CO = "CO"
    CT = "CT"
    DE = "DE"
    DC = "DC"
    FL = "FL"
    GA = "GA"
    HI = "HI"
    ID = "ID"
    IL = "IL"
    IN = "IN"
    IA = "IA"
    KS = "KS"
    KY = "KY"
    LA = "LA"
    ME = "ME"
    MD = "MD"
    MA = "MA"
    MI = "MI"
    MN = "MN"
    MS = "MS"
    MO = "MO"
    MT = "MT"
    NE = "NE"
    NV = "NV"
    NH = "NH"
    NJ = "NJ"
    NM = "NM"
    NY = "NY"
    NC = "NC"
    ND = "ND"
    OH = "OH"
    OK = "OK"
    OR = "OR"
    PA = "PA"
    PR = "PR"
    RI = "RI"
    SC = "SC"
    SD = "SD"
    TN = "TN"
    TX = "TX"
    UT = "UT"
    VT = "VT"
    VA = "VA"
    VI = "VI"
    WA = "WA"
    WV = "WV"
    WI = "WI"
    WY = "WY"

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
            return self
            # if country == "US" and postalCode is InstanceOf[UsPostalCode] or country == "CA" and postalCode is InstanceOf[CaPostalCode]:
            #     return self
            # else:
            #     print(type(postalCode))
            #     print(postalCode is InstanceOf[UsPostalCode])
            #     raise ValueError(f'postalCode value "{postalCode}" incompatible with country value "{country}"')
        else:
            raise ValueError(f'stateProv value "{stateProv}" incompatible with country value "{country}"')