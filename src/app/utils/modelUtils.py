from typing import Union
from re import compile

from faker.providers.address.en_CA import Provider as ProviderCA
from faker.providers.address.en_US import Provider as ProviderUS

from models.db.enumModels import StateEnum, ProvEnum

class CheckPostalCode:
    """
    A class for validating postal codes against
    country/stateProv constraints imported from Faker.
    """
    def __init__(self) -> None:
        """
        Initializes the class. Imports postcode prefixes
        for American and Canadian addresses.

        Args:
            None.

        Returns:
            None.
        """
        ca_postcode_prefixes = ProviderCA.provinces_postcode_prefixes
        us_postcode_prefixes = ProviderUS.states_postcode

        # Defines regex for country postal codes
        self.postalCodeRegexUS = compile(r"^[0-9]{5}[-](?:[0-9]{2}[0-9A-Z]{2}?)$")
        self.postalCodeRegexCA = compile(r"^[A-Z]{1}\d{1}[A-Z]{1}\s?\d{1}[A-Z]{1}\d{1}$")

        # Creates dict of postcode prefixes by country
        self.postcode_prefixes = {
            "CA": ca_postcode_prefixes,
            "US": us_postcode_prefixes
        }

    def postalCodeVerification(self, country:str, stateProv:str, postalCode:str) -> bool:
        postalCodeRange:Union[tuple[int,int], list] = self.pullValidPostalCodeRange(country=country, 
                                                                                    stateProv=stateProv)
        postcodeValid:bool = self.checkPostalCodeInRange(country=country, 
                                                         postalCodeRange=postalCodeRange, 
                                                         postalCode=postalCode)

        return postcodeValid

    def pullValidPostalCodeRange(self, country:str, stateProv:str) -> Union[tuple[int, int], list[str]]:
        country_valid_postcodes = self.postcode_prefixes[country]

        return country_valid_postcodes[stateProv]

    def checkPostalCodeInRange(self, country:str, postalCodeRange:list[tuple[int, int]], postalCode:str) -> bool:
        if country == "us" and 5 <= len(postalCode) <=10 :
            postalCode_3digit = int(postalCode[0:3])
            postalCode_4digit = int(postalCode[0:4])
            postalCode_5digit = int(postalCode[0:5])

            if postalCode_3digit in range(postalCodeRange[0], postalCodeRange[1]):
                return True
            elif postalCode_4digit in range(postalCodeRange[0], postalCodeRange[1]):
                return True
            elif postalCode_5digit in range(postalCodeRange[0], postalCodeRange[1]):
                return True
            else: 
                return False
            
        elif country == "ca" and 6 <= len(postalCode) <= 7:
            postalCode_1char = postalCode[0]

            if postalCode_1char in postalCodeRange:
                return True
            else: 
                return False
            
        else: 
            return False



