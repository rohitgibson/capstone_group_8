from uuid import uuid4
from time import sleep
import simplejson as json

from redis import Redis, ConnectionError
from redis.commands.search.query import Query
from pydantic import ValidationError

from models.api.modifyModels import AddAddress, UpdateAddress
from models.api.searchModels import SearchQuery, SearchResults

class RedisConnector:
    def __init__(self):
        print("REDIS CONNECTOR INIT")
        self.conn = Redis(decode_responses=True)
        self.createIndex()
        print("REDIS CONNECTOR STARTED")
    
    def createIndex(self):
        create_index_command = """
            FT.CREATE address_index
                ON JSON
                PREFIX 1 address
                SCHEMA $.firstName AS firstName TEXT SORTABLE $.lastName AS lastName TEXT SORTABLE $.addressLine1 AS addressLine1 TEXT SORTABLE $.addressLine2 AS addressLine2 TEXT SORTABLE $.city AS city TEXT SORTABLE $.stateProv AS stateProv TEXT SORTABLE $.postalCode AS postalCode TEXT SORTABLE $.country AS country TEXT SORTABLE
        """
        try:
            self.conn.execute_command(create_index_command)
        except Exception as e:
            print("Attempted to create index. Encountered an error:", e)

    def addRecord(self, data:dict):
        addAddressResponseCode = 0

        try:
            newAddress = dict(AddAddress(**data))
        except ValidationError:
            addAddressResponseCode = 400
            return addAddressResponseCode
        except Exception as e:
            addAddressResponseCode = 500
            return addAddressResponseCode
        
        try:
            data = dict(newAddress["data"])
            print(newAddress)
            self.conn.json().set(name=f"address:{str(uuid4())}",
                                 path="$",
                                 obj=data)    
        except ConnectionError as e:
            print("Redis Connection Error:", e)
            addAddressResponseCode = 500
            return addAddressResponseCode
        except Exception as e:
            print("Error:", e)
            addAddressResponseCode = 500
            return addAddressResponseCode

        print("Address added to Redis...")
        addAddressResponseCode = 201
        return addAddressResponseCode

    def searchData(self, data:dict):
        searchDataResponseCode = 0
        searchDataResponseData = {}

        # ERROR HANDLING BLOCK -- Checks for structural and logical issues with search query
        try:
            searchQuery = dict(SearchQuery(**data))
        except ValidationError:
            searchDataResponseCode = 400
            return searchDataResponseCode, searchDataResponseData
        except Exception as e:
            searchDataResponseCode = 500
            return searchDataResponseCode, searchDataResponseData
        
        # ERROR HANDLING BLOCK -- Checks for issues encountered during search query (likely to be Redis problems)
        try:
            if searchQuery["addressLine2"] != "":
                searchQueryFields = f"""@addressLine1:({searchQuery["addressLine1"]}) @addressLine2:{searchQuery["addressLine2"]} @city:({str(searchQuery["city"])}) @stateProv:{searchQuery["stateProv"]} @postalCode:{searchQuery["postalCode"]} @country:{searchQuery["country"]}"""
            else:
                searchQueryFields = f"""@addressLine1:({searchQuery["addressLine1"]}) @city:({str(searchQuery["city"])}) @stateProv:{searchQuery["stateProv"]} @postalCode:{searchQuery["postalCode"]} @country:{searchQuery["country"]}"""              
            searchQueryParams = f""""""
            searchQuery = searchQueryFields + searchQueryParams
            searchResults = self.conn.ft(index_name="address_index").search(Query(searchQuery)).docs
            searchResults = [{'key':result["id"],"data":json.loads(result["json"])} for result in searchResults]
        except ConnectionError as e:
            # print("Attempted to search index. Encountered a Redis error:", e)
            searchDataResponseCode = 500
            return searchDataResponseCode, searchDataResponseData
        except Exception as e:
            # print("Attempted to search index. Encountered an error:", e)
            searchDataResponseCode = 500
            return searchDataResponseCode, searchDataResponseData

        if searchResults != []:
            addressVerified = True
            searchDataResponseData = {
                "searchQuery": searchQuery,
                "addressVerified": addressVerified,
                "recommendedAddresses": searchResults
            }   
        else:
            addressVerified = False
            searchDataResponseData = {
                "searchQuery": searchQuery,
                "addressVerified": addressVerified
            }

        searchDataResponseCode = 200
        searchDataResponseData = dict(SearchResults(**searchDataResponseData))

        return searchDataResponseCode, searchDataResponseData
         
    def updateRecord(self, data:dict):
        try:
            updateAddress = dict(UpdateAddress(**data))
            key = updateAddress["key"]
            data = dict(updateAddress["data"])
            print(data)
            self.conn.json().set(name=f"{key}",
                                 path="$",
                                 obj=data)
        except ConnectionError as e:
            print("Redis Connection Error:", e)
            exit(1)
        except ValidationError as e:
            print("Pydantic Validation Error:", e)
            exit(1)
        except Exception as e:
            print("Error:", e)
            exit(1)

        print(f"Address updated in Redis for {key}")

    def deleteRecord(self, data:dict):
        pass



