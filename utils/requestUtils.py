import simplejson as json

class RequestUtils:
    def __init__(self):
        pass
    
    def processRequestData(self, data:bytes) -> dict:
        try:
            processedData = json.loads(data)
        except Exception as e:
            print("Exception in Request data:", e)
            processedData = {}

        return processedData

        