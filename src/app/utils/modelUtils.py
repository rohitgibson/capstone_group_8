from typing import Union
from re import compile

from faker.providers.address.en_CA import Provider as ProviderCA
from faker.providers.address.en_US import Provider as ProviderUS
import pandas as pd

from models.db.enumModels import StateEnum, ProvEnum

class CheckPostalCode:
    """
    A class for validating postal codes against
    country/stateProv constraints imported from Faker.
    """
    def __init__(self) -> None:
        """
        Initializes the class. Imports postcode prefixes for American 
        and Canadian addresses. Currently unused for US addresses
        because of uncertainty regarding ZIP code blocks assigned 
        to certain states.

        Args:
            None.

        Returns:
            None.
        """
        ca_postcode_prefixes = ProviderCA.provinces_postcode_prefixes
        us_postcode_prefixes = self.loadUSConstraints()

        # Defines regex for country postal codes
        self.postalCodeRegexUS = compile(r"^[0-9]{5}[-](?:[0-9]{2}[0-9A-Z]{2}?)$")
        self.postalCodeRegexCA = compile(r"^[A-Z]{1}\d{1}[A-Z]{1}\s?\d{1}[A-Z]{1}\d{1}$")

        # Creates dict of postcode prefixes by country
        self.postcode_prefixes = {
            "CA": ca_postcode_prefixes,
            "US": us_postcode_prefixes
        }

    def loadUSConstraints(self):
        faker_postcode_ranges = ProviderUS.states_postcode

        zip_df = pd.read_csv("./static/zips.csv")
        zip_df = zip_df.iloc[:,0:2].dropna(how="any").reset_index(drop=True)

        zip_df_updated = pd.DataFrame()
        zip_df_updated["zip_code_prefix"] = zip_df.iloc[:,1].apply(lambda x: str(x).split(" ")[-1]).apply(lambda y: str(y).replace("N", "").replace("U", ""))
        zip_df_updated["state"] = zip_df.iloc[:,1].apply(lambda x: str(x).split(" ")[-2])

        zip_df_updated = zip_df_updated[["zip_code_prefix", "state"]]
        zip_lambda = lambda zip_entries: {"state": zip_entries[0]["state"], "zip_prefixes":[(int(f"{zip_entry['zip_code_prefix']}00"),int(f"{zip_entry['zip_code_prefix']}99")) for zip_entry in zip_entries]+[faker_postcode_ranges[zip_entries[0]["state"]]]}
        zip_df_updated_grouper = zip_df_updated.groupby(pd.Grouper(key="state"), as_index=False)
        
        zip_list = list(map(zip_lambda, [group[1].to_dict(orient="records") for group in zip_df_updated_grouper]))

        return zip_list

    def postalCodeVerification(self, country:str, stateProv:str, postalCode:str) -> bool:
        postalCodeRange:Union[tuple[int,int], list] = self.pullValidPostalCodeRange(country=country, 
                                                                                    stateProv=stateProv)
        postcodeValid:bool = self.checkPostalCodeInRange(country=country, 
                                                         postalCodeRange=postalCodeRange, 
                                                         postalCode=postalCode)

        return postcodeValid

    def pullValidPostalCodeRange(self, country:str, stateProv:str) -> Union[tuple[int, int], list[str]]:
        country_valid_postcodes = self.postcode_prefixes[country]

        if country == "CA":
            return country_valid_postcodes[stateProv]
        elif country == "US":
            return list(filter(lambda country_valid_postcodes: country_valid_postcodes["state"] == stateProv, self.postcode_prefixes[country]))[0]["zip_prefixes"]

    def checkPostalCodeInRange(self, country:str, postalCodeRange:list[tuple[int, int]], postalCode:str) -> bool:
        if country == "US":
            postalCode_3digit = int(postalCode[0:3])
            postalCode_4digit = int(postalCode[0:4])
            postalCode_5digit = int(postalCode[0:5])

            if True in list(map(lambda postalCodeRange: self.mapZipRangeValid(postalCodeRange=postalCodeRange, postalCodeSubset=postalCode_3digit), postalCodeRange)):
                return True
            elif True in list(map(lambda postalCodeRange: self.mapZipRangeValid(postalCodeRange=postalCodeRange, postalCodeSubset=postalCode_4digit), postalCodeRange)):
                return True
            elif True in list(map(lambda postalCodeRange: self.mapZipRangeValid(postalCodeRange=postalCodeRange, postalCodeSubset=postalCode_5digit), postalCodeRange)):
                return True
            else: 
                return False
            
        elif country == "CA":
            postalCode_1char = postalCode[0]

            if postalCode_1char in postalCodeRange:
                return True
            else: 
                return False
            
        else: 
            return False

    def mapZipRangeValid(self, postalCodeRange: tuple[int, int], postalCodeSubset:str) -> bool:
        return postalCodeSubset in range(postalCodeRange[0], postalCodeRange[1])