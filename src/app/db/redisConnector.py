from uuid import uuid4
from time import sleep
from typing import Union, Any
import simplejson as json

from redis import Redis, ConnectionError
from redis.commands.search.query import Query
from pydantic import ValidationError

from utils.makeFuzzy import MakeFuzzy

from models.api.modifyModels import AddAddress, UpdateAddress, DeleteAddress
from models.api.searchModels import SearchQuery, SearchResults

from db.redisBackupManager import RedisBackupManager

class RedisConnector(RedisBackupManager):
    def __init__(self):
        print("REDIS CONNECTOR INIT")
        # Establishes Redis connection for all subsequent requests
        self.conn = Redis(decode_responses=True)
        # Attempts to create a search index
        self.createIndex()
        # Creates instance of MakeFuzzy util for RediSearch Levenshtein distance fuzzy matching
        self.makeFuzzy = MakeFuzzy()
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
            print("Created a new Redis index...")
        except Exception as e:
            print("Attempted to create index. Encountered an error:", e)

    def checkKeyExists(self, key:str) -> bool:
        try:
            key_check = self.conn.json().get(key)
            print(key_check)
        except Exception as e:
            print("Redis key check exception:", e)
            return False
        
        if key_check is not None:
            return True
        else:
            return False

    def addRecord(self, data:dict[str, Any]) -> tuple[int, str]:
        try:
            newAddress = AddAddress(**data).model_dump()
        except ValidationError as e:
            return 400, f"Address validation failed: {e}"
        except Exception as e:
            return 500, f"Miscellaneous server error: {e}. Please try again later."
        
        try:
            data = dict(newAddress["data"])
            self.conn.json().set(name=f"address:{str(uuid4())}",
                                 path="$",
                                 obj=data)    
        except ConnectionError as e:
            return 500, f"Database connection error: {e}. Please try again later."
        except Exception as e:
            return 500, f"Miscellaneous server error: {e}. Please try again later."

        return 201, "Address successfully added to Redis"

    def searchData(self, data:dict[str, Any]) -> tuple[int, dict[str,Any], str]:
        searchDataResponseData = {}

        # ERROR HANDLING BLOCK -- Checks for structural and logical issues with search query
        try:
            searchData = SearchQuery(**data).model_dump()
        except ValidationError as e:
            return 400, {}, f"Search validation failed: {e}"
        except Exception as e:
            return 500, {}, f"Miscellaneous server error: {e}"
        
        # ERROR HANDLING BLOCK -- Checks for issues encountered during search query (likely to be Redis problems)
        try:
            if searchData["addressLine2"] != "":
                searchQuery = f"""@addressLine1:({searchData["addressLine1"]}) @addressLine2:{searchData["addressLine2"]} @city:({str(searchData["city"])}) @stateProv:{searchData["stateProv"]} @postalCode:{searchData["postalCode"]} @country:{searchData["country"]}"""
            else:
                print(self.makeFuzzy.execute(query_text=searchData["postalCode"]))
                searchQuery = rf"""@addressLine1:"{searchData["addressLine1"]}" @city:({str(searchData["city"])}) @stateProv:({searchData["stateProv"]}) @postalCode:{self.makeFuzzy.execute(query_text=searchData["postalCode"])} @country:{searchData["country"]}"""       
            searchResults = self.conn.ft(index_name="address_index").search(Query(searchQuery)).docs
            searchResults = [{'key':result["id"],"data":json.loads(result["json"])} for result in searchResults]
        except ConnectionError as e:
            return 500, {}, f"Database connection error: {e}. Please try again later."
        except Exception as e:
            return 500, {}, f"Miscellaneous server error: {e}. Please try again later."

        # IF SEARCH EXECUTES WITHOUT ERROR -- Check for search results
        if searchResults != []:
            addressVerified = True
            searchDataResponseData = {
                "searchRequest": searchData,
                "addressVerified": addressVerified,
                "recommendedAddresses": searchResults
            }   
        else:
            addressVerified = False
            searchDataResponseData = {
                "searchRequest": searchData,
                "addressVerified": addressVerified
            }

        searchDataResponseData = SearchResults(**searchDataResponseData).model_dump()

        return 200, searchDataResponseData, "Address search/verification successful"
    
    # UPDATE RECORD  
    def updateRecord(self, data:dict[str, Any]) -> tuple[int, str]:
        # Performs model validation check on inbound data
        try:
            updateAddress = UpdateAddress(**data).model_dump()
        except ValidationError as e:
            return 400, f"Update validation failed: {e}"
        except Exception as e: 
            return 500, f"Miscellaneous server error: {e}"
        
        # Performs check on db to verify key exists 
        key = updateAddress["key"]
        key_exists:bool = self.checkKeyExists(key=key)
        if key_exists is False:
            return 404, f"Key {key} does not exist."
        else:
            pass

        # Key update logic
        try:
            data = dict(updateAddress["data"])
            print(data)
            self.conn.json().set(name=f"{key}",
                                 path="$",
                                 obj=data)
        except ConnectionError as e:
            # print("Redis Connection Error:", e)
            return 500, f"Database connection error: {e}. Please try again later."
        except Exception as e:
            # print("Error:", e)
            return 500, f"Miscellaneous server error: {e}. Please try again later."

        return 201, f"Address updated for {key}"

    def deleteRecord(self, data:dict[str, Any]) -> tuple[int, str]:

        try:
            deleteAddress = DeleteAddress(**data).model_dump()
        except ValidationError as e:
            return 400, f"Delete validation failed: {e}"
        except Exception as e: 
            return 500, f"Miscellaneous server error: {e}"

        # Performs check on db to verify key exists 
        key = deleteAddress["key"]
        key_exists:bool = self.checkKeyExists(key=key)
        if key_exists is False:
            return 404, f"Key {key} does not exist."
        else:
            pass

        try:
            key = deleteAddress["key"]
            self.conn.json().delete(key=f"{key}",
                                    path="$")
        except ConnectionError as e:
            return 500, f"Database connection error: {e}. Please try again later."
        except Exception as e:
            return 500, f"Miscellaneous server error: {e}. Please try again later."

        return 200, f"Successfully deleted {key}"



