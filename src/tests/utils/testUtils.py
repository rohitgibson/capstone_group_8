from random import randint

from faker import Faker

fakerGen = Faker(locale="en_US")

class AddressParser:
    def __init__(self) -> None:
        self.addressLine2Map = {
            "Apartment": "APT",
            "Basement": "BSMT",
            "#": "#",
            "Building": "BLDG",
            "Department": "DEPT",
            "Floor": "FL",
            "Front": "FRNT",
            "Hanger": "HNGR",
            "Key": "KEY",
            "Lobby": "LBBY",
            "Lot": "LOT",
            "Lower": "LOWR",
            "Office": "OFC",
            "Penthouse": "PH",
            "Pier": "PIER",
            "Rear": "REAR",
            "Room": "RM",
            "Side": "SIDE",
            "Slip": "SLIP",
            "Space": "SPC",
            "Stop": "STOP",
            "Suite": "STE",
            "Trailer": "TRLR",
            "Unit": "UNIT",
            "Upper": "UPPR"
        }

    def execute(self, address:str):
        address_line, city_line, stateprov_postalcode_line = self.splitAddress(address=address)

        # Processing the address line
        address_line_list = self.splitAddressLine(address_line=address_line)
        address_line_1, address_line_2 = self.parseAddressLineList(address_line_list=address_line_list)

        # Processing the city
        city = city_line.upper()

        # Processing stateprov and postal code
        state_prov, postal_code = self.splitStateProvPostalCode(stateprov_postalcode_line=stateprov_postalcode_line)

        try:
            return {
                "address":{
                    "addressLine1": address_line_1,
                    "addressLine2": address_line_2,
                    "city": city,
                    "stateProv": state_prov,
                    "postalCode": fakerGen.zipcode_in_state(state_abbr=str(state_prov))+"-"+str(randint(1000,9999)),
                    "country": "US"
                }
            }
        except Exception:
            return {
                "address":{
                    "addressLine1": address_line_1,
                    "addressLine2": address_line_2,
                    "city": city,
                    "stateProv": state_prov,
                    "postalCode": postal_code+"-"+str(randint(1000,9999)),
                    "country": "US"
                }
            }


    def splitAddress(self, address:str) -> tuple[str, str, str]:
        return address.replace(".", "").split(",")[0], address.split(",")[1], address.split(",")[2]

    def splitAddressLine(self, address_line:str) -> list[str]:
        return address_line.split(" ")
    
    def parseAddressLineList(self, address_line_list:list[str]) -> tuple[str, str]:
        addr_line_2_keyword_list = list(filter(lambda word: word.title() in list(self.addressLine2Map.keys()) or word.upper() in list(self.addressLine2Map.values()), address_line_list))

        # print(addr_line_2_keyword_list)
        

        if addr_line_2_keyword_list != []:
            address_line_1 = " ".join(address_line_list[0:address_line_list.index(str(addr_line_2_keyword_list[0]))]).upper()
            address_line_2 = " ".join(address_line_list[address_line_list.index(str(addr_line_2_keyword_list[0])):]).upper()
        else:
            address_line_1 = " ".join(address_line_list)
            address_line_2 = ""

        return address_line_1, address_line_2

    def splitStateProvPostalCode(self, stateprov_postalcode_line:str) -> tuple[str, str]:
        stateprov_postalcode_line = stateprov_postalcode_line.split(" ")

        # print(stateprov_postalcode_line)

        return stateprov_postalcode_line[-2], stateprov_postalcode_line[-1]
    
