from uuid import uuid4
from time import sleep
import simplejson as json

from redis import Redis, ConnectionError
from redis.commands.search.query import Query
from pydantic import ValidationError

from utils.makeFuzzy import MakeFuzzy

from models.api.modifyModels import AddAddress, UpdateAddress, DeleteAddress
from models.api.searchModels import SearchQuery, SearchResults

class RedisConnector:
    def __init__(self):
        print("REDIS CONNECTOR INIT")
        self.conn = Redis(decode_responses=True)
        self.createIndex()
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

    def addRecord(self, data:dict):
        addRecordResponseCode = 0

        try:
            newAddress = AddAddress(**data).model_dump()
        except ValidationError as e:
            print(e)
            addRecordResponseCode = 400
            return addRecordResponseCode
        except Exception as e:
            addRecordResponseCode = 500
            return addRecordResponseCode
        
        try:
            data = dict(newAddress["data"])
            print(newAddress)
            self.conn.json().set(name=f"address:{str(uuid4())}",
                                 path="$",
                                 obj=data)    
        except ConnectionError as e:
            # print("Redis Connection Error:", e)
            addRecordResponseCode = 500
            return addRecordResponseCode
        except Exception as e:
            # print("Error:", e)
            addRecordResponseCode = 500
            return addRecordResponseCode

        print("Address added to Redis...")
        addRecordResponseCode = 201
        return addRecordResponseCode


    def searchData(self, data:dict):
        searchDataResponseCode = 0
        searchDataResponseData = {}

        # ERROR HANDLING BLOCK -- Checks for structural and logical issues with search query
        try:
            searchData = SearchQuery(**data).model_dump()
        except ValidationError:
            searchDataResponseCode = 400
            return searchDataResponseCode, searchDataResponseData
        except Exception as e:
            searchDataResponseCode = 500
            return searchDataResponseCode, searchDataResponseData
        
        # ERROR HANDLING BLOCK -- Checks for issues encountered during search query (likely to be Redis problems)
        try:
            if searchData["addressLine2"] != "":
                searchQuery = f"""@addressLine1:({searchData["addressLine1"]}) @addressLine2:{searchData["addressLine2"]} @city:({str(searchData["city"])}) @stateProv:{searchData["stateProv"]} @postalCode:{searchData["postalCode"]} @country:{searchData["country"]}"""
            else:
                print(self.makeFuzzy.execute(query_text=searchData["postalCode"]))
                searchQuery = rf"""@addressLine1:"{searchData["addressLine1"]}" @city:({str(searchData["city"])}) @stateProv:({searchData["stateProv"]}) @postalCode:{self.makeFuzzy.execute(query_text=searchData["postalCode"])} @country:{searchData["country"]}"""
                print(searchQuery)              
            searchQueryParams:dict = {"RETURN ":"1"}
            searchResults = self.conn.ft(index_name="address_index").search(Query(searchQuery), query_params=searchQueryParams).docs
            print(searchResults)
            searchResults = [{'key':result["id"],"data":json.loads(result["json"])} for result in searchResults]
            print(searchResults)
        except ConnectionError as e:
            print("Attempted to search index. Encountered a Redis error:", e)
            searchDataResponseCode = 500
            return searchDataResponseCode, searchDataResponseData
        except Exception as e:
            print("Attempted to search index. Encountered an error:", e)
            searchDataResponseCode = 500
            return searchDataResponseCode, searchDataResponseData

        # IF SEARCH EXECUTES WITHOUT ERROR -- Check for search results
        if searchResults != []:
            addressVerified = True
            searchDataResponseData = {
                "searchQuery": searchData,
                "addressVerified": addressVerified,
                "recommendedAddresses": searchResults
            }   
        else:
            addressVerified = False
            searchDataResponseData = {
                "searchQuery": searchData,
                "addressVerified": addressVerified
            }

        searchDataResponseCode = 200
        searchDataResponseData = SearchResults(**searchDataResponseData).model_dump_json()

        return searchDataResponseCode, searchDataResponseData
    

    # UPDATE RECORD  
    def updateRecord(self, data:dict):
        updateRecordResponseCode = 0


        try:
            updateAddress = UpdateAddress(**data).model_dump()
        except ValidationError:
            updateRecordResponseCode = 400
            return updateRecordResponseCode
        except Exception: 
            updateRecordResponseCode = 500
            return updateRecordResponseCode


        try:
            key = updateAddress["key"]
            data = dict(updateAddress["data"])
            print(data)
            self.conn.json().set(name=f"{key}",
                                 path="$",
                                 obj=data)
        except ConnectionError as e:
            # print("Redis Connection Error:", e)
            updateRecordResponseCode = 500
            return updateRecordResponseCode
        except Exception as e:
            # print("Error:", e)
            updateRecordResponseCode = 500
            return updateRecordResponseCode


        print(f"Address updated in Redis for {key}")
        updateRecordResponseCode = 201
        return updateRecordResponseCode

    def deleteRecord(self, data:dict):
        deleteRecordResponseCode = 0

        
        try:
            deleteAddress = DeleteAddress(**data).model_dump()
        except ValidationError:
            deleteRecordResponseCode = 400
            return deleteRecordResponseCode
        except Exception: 
            deleteRecordResponseCode = 500
            return deleteRecordResponseCode


        try:
            key = deleteAddress["key"]
            self.conn.json().delete(key=f"{key}",
                                    path="$")
        except ConnectionError as e:
            # print("Redis Connection Error:", e)
            deleteRecordResponseCode = 500
            return deleteRecordResponseCode
        except Exception as e:
            # print("Error:", e)
            deleteRecordResponseCode = 500
            return deleteRecordResponseCode

        
        print(f"Successfully deleted {key}")
        deleteRecordResponseCode = 200
        return deleteRecordResponseCode



