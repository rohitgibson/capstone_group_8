# import datetime as dt
# from typing import Optional, List

from fastapi import FastAPI

from connections.redisConnector import RedisConnector

app = FastAPI()


test_dict = {
    "firstName": "John",
    "lastName": "Dow",
    "addressLine1": "2300 Windy Ridge",
    "addressLine2": "",
    "city": "Atlanta",
    "stateProv": "ID",
    "postalCode": "30339",
    "country": "US"
}

search_dict = {
    "addressLine1": "2300 Windy Ridge",
    "addressLine2": "",
    "city": "Atlanta",
    "stateProv": "GA",
    "postalCode": "30339",
    "country": "US"
}

redisConnector = RedisConnector()
# redisConnector.addData(test_dict)
# redisConnector.updateRecord(key="address:fc452f31-cde2-4518-80df-bbce8d34adef", data=test_dict)
print("Searching")
redisConnector.searchData(search_dict)








