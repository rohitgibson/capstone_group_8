from typing import Union, Any, Literal
from datetime import datetime as dt
import os

import simplejson as json
from pydantic import ValidationError

from models.api.responseModels import RequestResponse, AbortResponse

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
        if eval(str(self.getCurrentFlags(flag="verbose"))) is True:
            # if the verbose flag is True return the response message
            # in its entirety
            requestResponse = {
                "requestType": requestType,
                "requestData": requestData,
                "requestSuccess": requestSuccess,
                "responseTimestamp": dt.utcnow(),
                "responseStatusMsg": responseMsg,
                "responseData": responseData
            }
        else:
            requestResponse = {
                "requestType": requestType,
                "requestData": requestData,
                "requestSuccess": requestSuccess,
                "responseTimestamp": dt.utcnow(),
                "responseStatusMsg": responseMsg.split(":")[0],
                "responseData": responseData
            }

        # converts requestResponse dict data to JSON for API response
        requestResponse = RequestResponse(**requestResponse).model_dump_json()

        # returns requestResponse JSON data
        return requestResponse
    
    def processAbortResponse(self, responseCode:int, responseMsg:str):
        """
        Constructs an abort response dictionary, converts it to JSON 
        format, and returns the JSON-formatted string.

        Args:
            `responseCode`: 
                The response code for the abort response.
            `responseMsg`: 
                The response message for the abort response.

        Returns:
            The JSON-formatted abort response string.
        """

        # builds abortResponse dict from params
        abortResponse = {
            "responseStatusCode": int(responseCode),
            "responseStatusMsg": responseMsg
        }

        # converts abortResponse dict data to JSON for API response
        abortResponse = AbortResponse(**abortResponse).model_dump_json()

        # returns abortResponse data
        return abortResponse
    
    def getCurrentFlags(self, flag:Union[Literal["verbose"], Literal["validation"], Literal["redis-lock"]]):
        """
        Retrieves the current value of the specified AVS response flag.

        Args:
            `mode`: 
                The flag to retrieve.

        Returns:
            A boolean representing the current value of the specified flag.
        """

        if flag == "verbose":
            return os.environ.get("AVS_RESPONSE_VERBOSE", "False")
        elif flag == "validation":
            return os.environ.get("AVS_RESPONSE_VALIDATION", "True")
        elif flag == "redis-lock":
            return os.environ.get("AVS_REDIS_LOCK", "False")

    def setCurrentFlags(self, flag:Union[Literal["verbose"], Literal["validation"], Literal["redis-lock"]], flag_value:str):
        """
        Sets the specified AVS response flag to the given value.

        Args:
            `mode`: 
                The flag to set.
            `flag_value`: 
                The new value for the specified flag.
        """

        if flag == "verbose":
            os.environ["AVS_RESPONSE_VERBOSE"] = flag_value
        elif flag == "validation":
            os.environ["AVS_RESPONSE_VALIDATION"] = flag_value
        elif flag == "redis-lock":
            os.environ["AVS_REDIS_LOCK"] == flag_value
