from uuid import uuid4
from time import sleep
import simplejson as json

from redis import Redis, ConnectionError
from redis.commands.search.query import Query
from pydantic import ValidationError

from models.api.modifyModels import AddAddress, UpdateAddress
from models.api.searchModels import SearchQuery

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

    def searchData(self, data:dict):
        try:
            searchData = dict(SearchQuery(**data))
            if searchData["addressLine2"] != "":
                searchQueryFields = f"""@addressLine1:({searchData["addressLine1"]}) @addressLine2:{searchData["addressLine2"]} @city:({str(searchData["city"])}) @stateProv:{searchData["stateProv"]} @postalCode:{searchData["postalCode"]} @country:{searchData["country"]}"""
            else:
                searchQueryFields = f"""@addressLine1:({searchData["addressLine1"]}) @city:({str(searchData["city"])}) @stateProv:{searchData["stateProv"]} @postalCode:{searchData["postalCode"]} @country:{searchData["country"]}"""              
            searchQueryParams = f""""""
            searchQuery = searchQueryFields + searchQueryParams
            searchResults = self.conn.ft(index_name="address_index").search(Query(searchQuery)).docs
            searchResults = [{'key':result["id"],"data":json.loads(result["json"])} for result in searchResults]
            return searchResults
        except ConnectionError as e:
            print("Attempted to search index. Encountered a Redis error:", e)
            exit(1)
        except ValidationError as e:
            print("Attempted to search index. Encountered a Pydantic error:", e)
            exit(1)
        except Exception as e:
            print("Attempted to search index. Encountered an error:", e)
            exit(1)
        
    def addRecord(self, data:dict):
        try:
            newAddress = dict(AddAddress(**data))
            data = dict(newAddress["data"])
            print(newAddress)
            self.conn.json().set(name=f"address:{str(uuid4())}",
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

        print("Address added to Redis...")
         
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



