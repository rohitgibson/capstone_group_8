from uuid import uuid4
from time import sleep
import simplejson as json

# from redis_om import get_redis_connection
from redis import Redis, ConnectionError, from_url, Connection
from redis.commands.search.aggregation import AggregateRequest, Asc
from redis.commands.search.query import Query
from redis.lock import Lock
from pydantic import ValidationError

from models.api.addModels import Address
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
            searchCommand = self.conn.ft(index_name="address_index").search(Query(searchQuery)).docs
            searchCommand = [{'key':result["id"],"data":json.loads(result["json"])} for result in searchCommand]
            return searchCommand
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
            newAddress = dict(Address(**data))
            print(newAddress)
            self.conn.json().set(name=f"address:{str(uuid4())}",
                                 path="$",
                                 obj=newAddress)
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
         
    def updateRecord(self, key:str, data:dict):
        try:
            updateAddress = dict(Address(**data))
            print(updateAddress)
            self.conn.json().set(name=f"{key}",
                                 path="$",
                                 obj=updateAddress)
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

    def deleteRecord(self, key:str):
        pass

    def getRecord(self, key:str):
        pass

    # def connectionDisconnect(self):
    #     pass

