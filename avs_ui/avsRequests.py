from typing import Any
import simplejson 

import requests
from requests.auth import HTTPBasicAuth

from config.config import AVS_API_CONF

class AvsRequests:
    def __init__(self) -> None:
        self.request_session = requests.Session()


    def sendRequest(self, method:str, url:str, auth:HTTPBasicAuth, json:str) -> dict[str, Any]:
        try:
            request_object = requests.Request(method=method, url=url, auth=auth, json=json)
            request_prepped = request_object.prepare()
            request = self.request_session.send(request=request_prepped)
            
            request_data = simplejson.loads(str(request.content))
            
            return request_data
        except Exception as e:
            print(e)

            return {"requestSuccessful": False, 
                    "responseStatusMsg": "Issues were encountered while processing your request. Try again later."}
        

    def addRequest(self, request_data:dict[str, Any], credentials:dict[str, Any]):
        request_method = "POST"
        request_url = f"{AVS_API_CONF['tgt_uri']}{AVS_API_CONF['add_endpoint']}"
        request_basicauth = HTTPBasicAuth(username=credentials["username"],
                                          password=credentials["password"])
        request_json = simplejson.dumps(request_data)

        response_data = self.sendRequest(method=request_method,
                                         url=request_url,
                                         auth=request_basicauth,
                                         json=request_json)
        
        add_response_data = {
            "requestSuccessful": response_data["requestSuccessful"],
            "responseStatusMsg": response_data["responseStatusMsg"]
        }


        return add_response_data


    def searchRequest(self, request_data:dict[str, Any], credentials:dict[str, Any]):
        request_method = "GET"
        request_url = f"{AVS_API_CONF['tgt_uri']}{AVS_API_CONF['search_endpoint']}"
        request_basicauth = HTTPBasicAuth(username=credentials["username"],
                                          password=credentials["password"])
        request_json = simplejson.dumps(request_data)

        response_data = self.sendRequest(method=request_method,
                                         url=request_url,
                                         auth=request_basicauth,
                                         json=request_json)
        
        search_response_data = {
            "requestSuccessful": response_data["requestSuccessful"],
            "responseStatusMsg": response_data["responseStatusMsg"],
            "addressVerified": response_data["responseData"]["addressVerified"],
            "recommendedAddresses": response_data["responseData"]["recommendedAddresses"]
        }

        return search_response_data
    

    def updateRequest(self, request_data:dict[str, Any], credentials:dict[str, Any]):
        request_method = "POST"
        request_url = f"{AVS_API_CONF['tgt_uri']}{AVS_API_CONF['update_endpoint']}"
        request_basicauth = HTTPBasicAuth(username=credentials["username"],
                                          password=credentials["password"])
        request_json = simplejson.dumps(request_data)

        response_data = self.sendRequest(method=request_method,
                                         url=request_url,
                                         auth=request_basicauth,
                                         json=request_json)
        
        update_response_data = {
            "requestSuccessful": response_data["requestSuccessful"],
            "responseStatusMsg": response_data["responseStatusMsg"]
        }

        return update_response_data


    def deleteRequest(self, request_data:dict[str, Any], credentials:dict[str, Any])  -> dict[str, Any]:
        request_method = "POST"
        request_url = f"{AVS_API_CONF['tgt_uri']}{AVS_API_CONF['delete_endpoint']}"
        request_basicauth = HTTPBasicAuth(username=credentials["username"],
                                          password=credentials["password"])
        request_json = simplejson.dumps(request_data)

        response_data = self.sendRequest(method=request_method,
                                         url=request_url,
                                         auth=request_basicauth,
                                         json=request_json)
        
        delete_response_data = {
            "requestSuccessful": response_data["requestSuccessful"],
            "responseStatusMsg": response_data["responseStatusMsg"]
        }

        return delete_response_data


