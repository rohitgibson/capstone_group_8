from base64 import b64decode

from quart import Blueprint, request, Response

from db.redisConnector import RedisConnector
from auth.auth import HTTPBasicAuth
from utils.requestUtils import RequestUtils

address_blueprint = Blueprint("address", __name__)

redisConnector = RedisConnector()
requestUtils = RequestUtils()
auth = HTTPBasicAuth()

# ENDPOINT - add address
@address_blueprint.route("/api/address/modify/add", methods=["POST"])
async def addAddress():
    permitted_roles = ["root", "admin"]
    # Loads request auth headers
    auth.authUser(permitted_roles=permitted_roles,
                  auth_data=rf"{request.authorization}")
    # Loads data from request
    data_nonjson:bytes = await request.get_data()
    data_json:bytes = await request.get_json()
    # Converts data to Python dictionary
    processedData = requestUtils.processRequestData(data_nonjson=data_nonjson, data_json=data_json, origin="add_address")
    # Adds data to Redis db
    addRecordResponseCode, addRecordResponseMsg = redisConnector.addRecord(data=processedData)
    # Sets response data
    response_data = requestUtils.processResponse(requestType="add_address",
                                                 requestData=processedData,
                                                 responseCode=addRecordResponseCode,
                                                 responseMsg=addRecordResponseMsg,
                                                 responseData=None)
    # Sets response data mimetype
    response_mimetype = "application/json"
    # Sets response HTTP status code
    response_status_code = addRecordResponseCode
    # Creates response object
    response = Response(response=response_data,
                        status=response_status_code,
                        mimetype=response_mimetype)
    # Returns response object
    return response


# ENDPOINT - search address
@address_blueprint.route("/api/address/search", methods=["GET"])
async def searchAddress():
    permitted_roles = ["root", "admin", "basic"]
    # Loads request auth headers
    auth.authUser(permitted_roles=permitted_roles,
                  auth_data=rf"{request.authorization}")
    # Loads data from request
    data_nonjson:bytes = await request.get_data()
    data_json:bytes = await request.get_json()
    # Converts data to Python dictionary
    processedData = requestUtils.processRequestData(data_nonjson=data_nonjson, data_json=data_json, origin="search_address")
    # Sends search query to Redis
    searchDataResponseCode, searchDataResponseData, searchRequestMsg = redisConnector.searchData(data=processedData)
    # Sets response data
    response_data = requestUtils.processResponse(requestType="search_address",
                                                 requestData=processedData,
                                                 responseCode=searchDataResponseCode,
                                                 responseMsg=searchRequestMsg,
                                                 responseData=searchDataResponseData)
    # Sets response data mimetype
    response_mimetype = "application/json"
    # Sets response HTTP status code
    response_status_code = searchDataResponseCode
    # Creates response object
    response = Response(response=response_data,
                        status=response_status_code,
                        mimetype=response_mimetype)
    # Returns response object
    return response


# ENDPOINT - update address
@address_blueprint.route("/api/address/modify/update", methods=["POST"])
async def updateAddress():
    permitted_roles = ["root", "admin"]
    # Loads request auth headers
    auth.authUser(permitted_roles=permitted_roles,
                  auth_data=rf"{request.authorization}")
    # Loads data from request
    data_nonjson:bytes = await request.get_data()
    data_json:bytes = await request.get_json()
    # Converts data to Python dictionary
    processedData = requestUtils.processRequestData(data_nonjson=data_nonjson, data_json=data_json, origin="update_address")
    # Updates data in Redis
    updateRecordResponseCode, updateRecordResponseMsg = redisConnector.updateRecord(data=processedData)
    # Sets response data
    response_data = requestUtils.processResponse(requestType="update_address",
                                                 requestData=processedData,
                                                 responseCode=updateRecordResponseCode,
                                                 responseMsg=updateRecordResponseMsg,
                                                 responseData=None)
    # Sets response data mimetype
    response_mimetype = "application/json"
    # Sets response HTTP status code
    response_status_code = updateRecordResponseCode
    # Creates response object
    response = Response(response=response_data,
                        status=response_status_code,
                        mimetype=response_mimetype)
    # Returns response object
    return response


# ENDPOINT - delete address
@address_blueprint.route("/api/address/modify/delete", methods=["POST"])
async def deleteAddress():
    permitted_roles = ["root", "admin"]
    # Loads request auth headers
    auth.authUser(permitted_roles=permitted_roles,
                  auth_data=rf"{request.authorization}")
    # Loads data from request
    data_nonjson:bytes = await request.get_data()
    data_json:bytes = await request.get_json()
    # Converts data to Python dictionary
    processedData = requestUtils.processRequestData(data_nonjson=data_nonjson, data_json=data_json, origin="delete_address")
    # Deletes data in Redis
    deleteRecordResponseCode, deleteRecordResponseMsg = redisConnector.deleteRecord(data=processedData)
    # Sets response data
    response_data = requestUtils.processResponse(requestType="delete_address",
                                                 requestData=processedData,
                                                 responseCode=deleteRecordResponseCode,
                                                 responseMsg=deleteRecordResponseMsg,
                                                 responseData=None)
    # Sets response data mimetype
    response_mimetype = "application/json"
    # Set response HTTP status code
    response_status_code = deleteRecordResponseCode
    # Creates response object
    response = Response(response=response_data,
                        status=response_status_code,
                        mimetype=response_mimetype)
    # Returns response object
    return response
