from uuid import uuid4
from time import sleep
from typing import Any

import simplejson as json
from redis import Redis, ConnectionError
from redis.commands.search.query import Query
from pydantic import ValidationError

from utils.makeFuzzy import MakeFuzzy

from models.api.modifyModels import AddAddress, DeleteAddress, UpdateAddress
from models.api.searchModels import SearchAddress, SearchResults
from utils.requestUtils import RequestUtils

class RedisConnector:
    """
    Handles all interactions with RedisDB from defining connection parameters
    to the Add, Validate/Search, Update, and Delete address use cases.    
    """

    def __init__(self):        
        # Establishes Redis connection for all subsequent requests
        self.conn = Redis(host="redis", port="6379", decode_responses=True)

        # Attempts to create a search index
        self.createIndex()

        # Creates instance of MakeFuzzy util for RediSearch Levenshtein distance fuzzy matching
        self.makeFuzzy = MakeFuzzy()

        print("Successfully started Redis connector class.")
        # logging.info("Successfully started Redis connector class.")
    
    # keeping just in case we need names again: $.firstName AS firstName TEXT SORTABLE $.lastName AS lastName TEXT SORTABLE
    def createIndex(self):
        """
        Attempts to create a Redis index.

        Args:
            None.

        Returns:
            None.
        """

        # Create the index creation command string 
        create_index_command = """
            FT.CREATE address_index
                ON JSON
                PREFIX 1 address
                SCHEMA $.addressLine1 AS addressLine1 TEXT SORTABLE 
                $.addressLine2 AS addressLine2 TEXT SORTABLE 
                $.city AS city TEXT SORTABLE 
                $.stateProv AS stateProv TEXT SORTABLE 
                $.postalCode AS postalCode TEXT SORTABLE 
                $.country AS country TEXT SORTABLE"""
        
        # Try to create the index
        try:
            self.conn.execute_command(create_index_command)
            print("Created a new Redis index...")
            # logging.info("Created a new Redis index...")
        except Exception as e:
            print("Attempted to create index. Encountered an error:", e)
            # logging.error("Attempted to create index. Encountered an error:", e)
        
    def checkKeyExists(self, key: str) -> bool:
        """
        Performs check on whether a particular key exists (for update & delete requests).
        
        Args:
            ``key``: 
                Key for record in Redis DB
        
        Returns:
            A boolean indicating whether the key exists.
        """

        # Try to get the value of the key using the json().get() command.
        try:
            key_check = self.conn.json().get(key)
        except Exception as e:
            # Log the error message and return False if an unexpected error occurs.
            print("Redis key check exception:", e)
            return False
        
        # If the key_check variable is not None, then the key exists.
        if key_check is not None:
            return True
        
        # Otherwise, the key does not exist.
        else:
            return False

    def addRecord(self, data: dict[str, Any]) -> tuple[int, str]:
        """
        Processes Redis record add request.

        Args:
            `data`: 
                API request data (converted to dict)

        Returns:
            A tuple of (status code, message)
        """

        # Validate the address data using the AddAddress model.
        try:
            newAddress = AddAddress(**data).model_dump(mode="JSON")["address"]
        except ValidationError as e:
            # Return a 400 status code and an error message if the address data is invalid.
            return 400, f"Address validation failed: {e}"
        except Exception as e:
            # Return a 500 status code and an error message if an unexpected error occurs.
            return 500, f"Miscellaneous server error: {e}. Please try again later."
        
        # Set the address record in Redis using the json().set() command.
        try:
            self.conn.json().set(name=f"address:{str(uuid4())}",
                                 path="$",
                                 obj=newAddress)    
        except ConnectionError as e:
            # Return a 500 status code and an error message if a database connection error occurs.
            return 500, f"Database connection error: {e}. Please try again later."
        except Exception as e:
            # Return a 500 status code and an error message if an unexpected error occurs.
            return 500, f"Miscellaneous server error: {e}. Please try again later."
        
        # Reindex for search if address successfully added
        self.createIndex()

        # Return a 201 status code and a success message if the address record was successfully added to Redis.
        return 201, "Address successfully added to Redis"
    
    def bulkAddRecord(self, bulkData: list[dict[str, Any]]) -> tuple[int, str]:
        """
        Processes bulk add request for mass data ingest and recovery

        Args:
            `bulkData`: 
                Iterable address data to be added to RedisDB

        Returns:
            A boolean indicating whether the operation was successful.      
        """

        # Create a list to store the status codes of all bulk add operations.
        all_status_codes = []

        # Iterate over the bulk data and call the addRecord() method for each address.
        for address in bulkData:
            data = {"address": address}
            status_code, msg = self.addRecord(data=data)

            # Add the status code of the current bulk add operation to the list.
            all_status_codes.append(status_code)

            print(msg)

        # Attempts to create a search index
        self.createIndex()

        # If something other than a 201 status code is in the list, then some or all
        # of the bulk add operations were unsuccessful.
        if not 201 in all_status_codes:

            # If some of the bulk add operations were successful, return a message
            # indicating that.
            if 201 in all_status_codes:
                return 201, "Some but not all bulk add operations were successful."
            
            # Otherwise, return a message indicating that all of the bulk add operations
            # were unsuccessful.
            else:
                return 400, "All bulk add operations were unsuccessful."
            
        # Otherwise, all of the bulk add operations were successful.
        else:
            return 400, "All bulk add operations were successful."
            

    def searchData(self, data: dict[str, Any]) -> tuple[int, dict[str,Any], str]:
        """
        Searches for addresses in Redis using the Fuzzy Search feature and returns
        the search results and verification status.

        Args:
            `data`:
                API request data (converted to dict)

        Returns:
            A tuple of (status code, a dictionary containing the search results and 
            verification status, an error message).
        """

        # Performs model validation check on inbound data
        try:
            searchData = SearchAddress(**data).model_dump()["address"]
        except ValidationError as e:
            return 400, {}, f"Search validation failed: {e}"
        except Exception as e:
            return 500, {}, f"Miscellaneous server error: {e}"
        
        # Construct the Redis search query.
        if searchData["addressLine2"] != "":
            searchQuery = f"""
            @addressLine1:({self.makeFuzzy.execute(query_text=searchData["addressLine1"],
                                                   wildcard_pattern="%")}) 
            @addressLine2:{self.makeFuzzy.execute(query_text=searchData["addressLine2"],
                                                  wildcard_pattern="%")} 
            @city:({self.makeFuzzy.execute(query_text=searchData["city"],
                                           wildcard_pattern="%")}) 
            @stateProv:{self.makeFuzzy.execute(query_text=searchData["stateProv"],
                                               wildcard_pattern="%")} 
            @postalCode:{self.makeFuzzy.execute(query_text=searchData["postalCode"],
                                                wildcard_pattern="%%")} 
            @country:{self.makeFuzzy.execute(query_text=searchData["country"],
                                             wildcard_pattern="%")}"""
        else:
            searchQuery = rf"""
            @addressLine1:({self.makeFuzzy.execute(query_text=searchData["addressLine1"],
                                                   wildcard_pattern="%")}) 
            @city:({self.makeFuzzy.execute(query_text=searchData["city"],
                                           wildcard_pattern="%")}) 
            @stateProv:({self.makeFuzzy.execute(query_text=searchData["stateProv"],
                                                wildcard_pattern="%")}) 
            @postalCode:{self.makeFuzzy.execute(query_text=searchData["postalCode"],
                                                wildcard_pattern="%%")} 
            @country:{self.makeFuzzy.execute(query_text=searchData["country"],
                                             wildcard_pattern="%")}"""       

        # Search for addresses in Redis.
        try:
            searchResults = self.conn.ft(index_name="address_index").search(Query(searchQuery)).docs
        except ConnectionError as e:
            # Return a 500 status code and an error message if a database 
            # connection error occurs.
            return 500, {}, f"Database connection error: {e}. Please try again later."
        except Exception as e:
            # Return a 500 status code and an error message if an unexpected
            # error occurs.
            return 500, {}, f"Miscellaneous server error: {e}. Please try again later."
        
        # Convert the search results to a list of dictionaries.
        searchResults = [{'key':result["id"],"address":json.loads(result["json"])} for result in searchResults]

        print(searchResults)

        # Check if the search results are empty.
        if searchResults != []:
            # The address is verified if there are search results.
            addressVerified = True

            # Create a dictionary containing the search request, address 
            # verification status, and recommended addresses.
            searchDataResponseData = {
            "searchRequest": searchData,
            "addressVerified": addressVerified,
            "recommendedAddresses": searchResults
            }
        else:
            # The address is not verified if there are no search results.
            addressVerified = False

            # Create a dictionary containing the search request and address verification status.
            searchDataResponseData = {
            "searchRequest": searchData,
            "addressVerified": addressVerified
            }

        # Convert the search data response dictionary to a JSON object.
        searchDataResponseData = SearchResults(**searchDataResponseData).model_dump(mode="JSON")

        # Return the search results and verification status.
        return 200, searchDataResponseData, "Address search/verification successful"
    
    def updateRecord(self, data: dict[str, Any]) -> tuple[int, str]:
        """
        Processes Redis record update request.

        Args:
            `data`: 
                API request data (converted to dict)

         Returns:
            A tuple of (status code, message)
        """

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
            return 404, f"Key does not exist."
        else:
            pass

        # Key update logic
        try:
            address = updateAddress["address"]
            self.conn.json().set(name=f"{key}",
                                 path="$",
                                 obj=address)
        except ConnectionError as e:
            return 500, f"Database connection error: {e}. Please try again later."
        except Exception as e:
            # logging.error(f"Error updating record: {e}")
            return 500, f"Miscellaneous server error: {e}. Please try again later."

        return 201, f"Address updated for {key}"

    def deleteRecord(self, data: dict[str, Any]) -> tuple[int, str]:
        """
        Processes Redis record deletion request.

        Args:
            `data`: 
                API request data (converted to dict)

        Returns:
            A tuple of (status code, message)
        """

        try:
            deleteAddress = DeleteAddress(**data).model_dump()
        except ValidationError as e:
            return 400, f"Delete validation failed: {e}"
        except Exception as e: 
            return 500, f"Miscellaneous server error: {e}"

        key = deleteAddress["key"]
        key_exists:bool = self.checkKeyExists(key=key)
        if key_exists is False:
            return 404, f"Key does not exist."
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
    
    def deleteAllRecords(self) -> tuple[int, str]:
        try:
            self.conn.flushall()
            self.createIndex()
        except ConnectionError as e:
            return 500, f"Database connection error: {e}. Please try again later."
        except Exception as e:
            return 500, f"Miscellaneous server error: {e}. Please try again later."


        return 200, f"Successfully deleted all records."



