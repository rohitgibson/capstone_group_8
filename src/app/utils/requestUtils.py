from typing import Union, Any
from datetime import datetime as dt

import simplejson as json
from pydantic import ValidationError

from models.api.responseModels import RequestResponse

class RequestUtils:
    """
    A class of helper scripts for processing request and 
    response data for the AVS API.
    """

    def __init__(self):
        """Initializes a new RequestUtils instance."""
        pass
    
    def processRequestData(self, data_nonjson: bytes, data_json: bytes, origin: str) -> dict[str, Any]:
        """
        Inbound requests for all endpoints error if data
        is either not present or in the wrong format. This
        script attempts to convert inbound JSON request data
        to a Python dictionary. Upon failing (if data isn't 
        in the correct format), data is returned as an empty dictionary.

        Args:
            ``data``: 
                The request body (as bytes).
            ``origin``: 
                The origin use case of the request (e.g. 'search'). 
                (Currently unused but retained in case future
                model/schema changes require additional processing
                dependent on the origin use case.)

        Returns:
            A dictionary of the processed request data.
        """

        # Attempts to convert data from JSON object to Python dict.
        try:
            processedData = dict(json.loads(data_nonjson))
        except Exception as e:
            # If error encountered in JSON conversion process, return
            # empty dict to prevent errors in request logic.
            # logging.error("Exception in Request data:", e)
            try:
                processedData = dict(json.loads(data_json))
            except Exception as e:
                processedData = {}


        # Returns dict of processed inbound request data.
        return processedData
    
    def processResponse(self, requestType: str, requestData: dict, responseCode: int, responseMsg: str, responseData: Union[dict, None]) -> str:
        """
        Standardizes outbound responses. This was implemented to
        streamline AVS UI development by (1) simplifying any
        request response parsing logic, (2) adding a 'requestSuccess'
        field to the model to show whether the request succeeded (or failed)
        at a glance, and (3) show a response status message that can
        be shown to and end user (while more detailed information is
        logged for devs).

        Args:
            ``requestType``: 
                The origin use case for the request/response data.
            ``requestData``: 
                The data that was sent with the request.
            ``responseCode``: 
                The HTTP response code returned by RedisConnector.
            ``responseMsg``: 
                The HTTP response message returned by RedisConnector.
            ``responseData``: 
                The response data from a search/verification request
                returned by RedisConnector.

        Returns:
            A JSON string of the processed response data.
        """
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

        # sets responseData variable
        if responseData is None:
            responseData = {}
        else:
            responseData = responseData

        # builds requestResponse data from previously set variables
        requestResponse = {
            "requestType": requestType,
            "requestData": requestData,
            "requestSuccess": requestSuccess,
            "responseTimestamp": dt.utcnow(),
            "responseStatusMsg": responseMsg,
            "responseData": responseData
        }

        # converts addResponse dict data to JSON for API response
        requestResponse = RequestResponse(**requestResponse).model_dump_json()

        # returns addResponse JSON data
        return requestResponse
    
