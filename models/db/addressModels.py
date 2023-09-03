from typing import Optional, Union, Any
from enum import Enum
from uuid import uuid4

# from redis_om import HashModel, VectorFieldOptions, Field
from pydantic import BaseModel, ValidationError, model_validator, field_validator, constr, Field

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
    firstName: str = Field(constr(strip_whitespace=True))
    lastName: str = Field(constr(strip_whitespace=True))
    addressLine1: str = Field(constr(strip_whitespace=True))
    addressLine2: str = Field(constr(strip_whitespace=True))
    city: str = Field(constr(strip_whitespace=True))
    stateProv: Union[StateEnum, ProvEnum] = Field(constr(strip_whitespace=True, to_upper=True))
    postalCode: str = Field(constr(strip_whitespace=True, to_upper=True))
    country: CountryEnum

    # Checks that stateProv enum is compatible with country enum 
    @model_validator(mode='after')
    def check_stateProv_valid(self) -> 'Address':
        stateProv = self.stateProv
        country = self.country

        if country == "US" and type(stateProv) == StateEnum or country == "CA" and type(stateProv) == ProvEnum:
            return self
        else:
            raise ValueError(f'stateProv value "{stateProv}" incompatible with country value "{country}"')