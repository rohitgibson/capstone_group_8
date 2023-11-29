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
        """
        This function reads a CSV file containing ZIP code prefixes 
        and corresponding states, converts the data into a suitable 
        format, and groups the data by state. It then returns a list 
        of ZIP code range information for each state.

        Returns:
            A list of ZIP code range information for each US state.
        """
        # Loads ZIP code constraints from Faker (these are
        # imperfect, so we're using messy USPS data to add
        # what Faker is missing)
        faker_postcode_ranges = ProviderUS.states_postcode

        # Load ZIP code data from CSV file
        zip_df = pd.read_csv("./static/zips.csv")
        
        # Drop rows with missing values and reset index
        zip_df = zip_df.iloc[:,0:2].dropna(how="any").reset_index(drop=True)

        # Extract ZIP code prefixes and states from the data
        zip_df_updated = pd.DataFrame()
        zip_df_updated["zip_code_prefix"] = zip_df.iloc[:,1].apply(lambda x: str(x).split(" ")[-1]).apply(lambda y: str(y).replace("N", "").replace("U", ""))
        zip_df_updated["state"] = zip_df.iloc[:,1].apply(lambda x: str(x).split(" ")[-2])

        # Group ZIP code information by state
        zip_df_updated = zip_df_updated[["zip_code_prefix", "state"]]
        zip_lambda = lambda zip_entries: {"state": zip_entries[0]["state"], "zip_prefixes":[(int(f"{zip_entry['zip_code_prefix']}00"),int(f"{zip_entry['zip_code_prefix']}99")) for zip_entry in zip_entries]+[faker_postcode_ranges[zip_entries[0]["state"]]]}
        zip_df_updated_grouper = zip_df_updated.groupby(pd.Grouper(key="state"), as_index=False)
        
        # Convert grouped data into a list of ZIP code range information
        zip_list = list(map(zip_lambda, [group[1].to_dict(orient="records") for group in zip_df_updated_grouper]))

        return zip_list

    def postalCodeVerification(self, country:str, stateProv:str, postalCode:str) -> bool:
        """
        Verifies whether a given postal code is valid for a 
        specific country, state, or province.

        Args:
            `country`: 
                The country code (e.g., "US", "CA")
            `stateProv`: 
                The state or province code (e.g., "NY", "ON")
            `postalCode`: 
                The postal code to verify

        Returns:
            A boolean that is True if the postal code is 
            valid, False otherwise.
        """

        # Retrieve the valid postal code range for the specified location
        postalCodeRange:Union[tuple[int,int], list] = self.pullValidPostalCodeRange(country=country, 
                                                                                    stateProv=stateProv)
        
        # Verify whether the postal code falls within the valid range
        postcodeValid:bool = self.checkPostalCodeInRange(country=country, 
                                                         postalCodeRange=postalCodeRange, 
                                                         postalCode=postalCode)

        return postcodeValid

    def pullValidPostalCodeRange(self, country:str, stateProv:str) -> Union[list[tuple[int, int]], list[str]]:
        """
        Retrieves the valid postal code range for a given 
        country and state/province.

        Args:
            `country`: 
                The country code (e.g., "US", "CA")
            `stateProv`: 
                The state or province code (e.g., "NY", "ON")

        Returns:
            The valid postal code range for the specified 
            country and state/province.
        """

        # Obtain the valid postal codes for the given country
        country_valid_postcodes = self.postcode_prefixes[country]

        # Handle different postal code formats for US and CA
        if country == "CA":
            return country_valid_postcodes[stateProv]
        elif country == "US":
            # Filter the valid postal codes for the specified 
            # state/province
            return list(filter(lambda country_valid_postcodes: country_valid_postcodes["state"] == stateProv, self.postcode_prefixes[country]))[0]["zip_prefixes"]

    def checkPostalCodeInRange(self, country:str, postalCodeRange:list[tuple[int, int]], postalCode:str) -> bool:
        """
        Verifies whether a given postal code is within the valid 
        postal code range for a specific country and state/province.

        Args:
            `country`: 
                The country code (e.g., "US", "CA")
            `postalCodeRange`: 
                The valid postal code range for the specified 
                country and state/province
            `postalCode`: 
                The postal code to verify

        Returns:
            A boolean that returns True if the postal code is 
            within the range, False otherwise.
        """

        # Convert the postal code to different subsets based on 
        # the country
        if country == "US":
            postalCode_3digit = int(postalCode[0:3])
            postalCode_4digit = int(postalCode[0:4])
            postalCode_5digit = int(postalCode[0:5])
            
            # Check if the postal code subset is within the 
            # valid range for each subset length
            if True in list(map(lambda postalCodeRange: self.mapZipRangeValid(postalCodeRange=postalCodeRange, postalCodeSubset=postalCode_3digit), postalCodeRange)):
                return True
            elif True in list(map(lambda postalCodeRange: self.mapZipRangeValid(postalCodeRange=postalCodeRange, postalCodeSubset=postalCode_4digit), postalCodeRange)):
                return True
            elif True in list(map(lambda postalCodeRange: self.mapZipRangeValid(postalCodeRange=postalCodeRange, postalCodeSubset=postalCode_5digit), postalCodeRange)):
                return True
            else: 
                return False
            
        elif country == "CA":
            # Checks the first letter of the Canadian postal
            # code against the valid postal code range for 
            # the province
            postalCode_1char = postalCode[0]

            if postalCode_1char in postalCodeRange:
                return True
            else: 
                return False
            
        else: 
            return False

    def mapZipRangeValid(self, postalCodeRange: tuple[int, int], postalCodeSubset:str) -> bool:
        """
        Checks whether a given postal code subset falls 
        within a specified postal code range.

        Args:
            `postalCodeRange`: 
                A tuple containing the valid postal code range
            `postalCodeSubset`: 
                The postal code subset to check

        Returns:
            A boolean that is True if the postal code 
            subset is within the range, False otherwise.
        """

        # Check if the postal code subset falls within the 
        # specified range
        return postalCodeSubset in range(postalCodeRange[0], postalCodeRange[1])