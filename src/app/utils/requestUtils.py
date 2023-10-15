import simplejson as json

from pydantic import ValidationError

from models.api.modifyModels import RequestResponse

class RequestUtils:
    def __init__(self):
        pass
    
    def processRequestData(self, data:bytes, origin:str) -> dict:
        try:
            processedData = json.loads(data)
        except Exception as e:
            print("Exception in Request data:", e)
            processedData = {}

        return processedData
    
    def processResponse(self, requestType:str, requestData:dict, responseCode:int, responseMsg:str):
        # sets requestType variable
        requestType = requestType
        
        # sets requestData variable
        requestData = requestData

        # sets requestSuccess variable
        if responseCode not in [200, 201]:
            requestSuccess = False
        else:
            requestSuccess = True

        # sets requestMsg variable
        responseMsg = responseMsg

        # builds requestResponse data from previously set variables
        requestResponse = {
            "requestType": requestType,
            "requestData": requestData,
            "requestSuccess": requestSuccess,
            "responseMsg": responseMsg
        }

        # converts addResponse dict data to JSON for API response
        requestResponse = RequestResponse(**requestResponse).model_dump_json()

        # returns addResponse JSON data
        return requestResponse
    
