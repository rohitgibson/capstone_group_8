from asyncio import get_event_loop

from quart import Quart, request, Response, abort
from quart.utils import run_sync

from db.redisConnector import RedisConnector
from auth.authContext import AuthContext
from utils.requestUtils import RequestUtils

# Inits quart app class
app = Quart(__name__)

# Inits helper classes for DB, request handling, and auth
redisConnector = RedisConnector()
requestUtils = RequestUtils()
authContext = AuthContext()

# Inits worker for keeping Redis from dying
# @run_sync
async def startup():
    loop = get_event_loop()
    loop.create_task(redisConnector.healthCheck())

# ENDPOINT - add address
@app.route("/api/address/add", methods=["POST"])
async def addAddress():
    permitted_roles = ["admin"]
    # Loads request auth headers
    authContext.authUser(permitted_roles=permitted_roles,
                         auth_data=request.authorization)
    # Loads data from request
    data:bytes = await request.get_data()
    # Converts data to Python dictionary
    processedData = requestUtils.processRequestData(data=data, origin="add")
    # Adds data to Redis db
    addRecordResponseCode, addRecordResponseMsg = redisConnector.addRecord(data=processedData)
    # Sets response data
    response_data = requestUtils.processResponse(requestType="add",
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
@app.route("/api/address/search", methods=["GET"])
async def searchAddress():
    permitted_roles = ["admin", "basic"]
    # Loads request auth headers
    authContext.authUser(permitted_roles=permitted_roles,
                         auth_data=request.authorization)
    # Loads data from request
    data:bytes = await request.get_data()
    # Loads data from request
    processedData = requestUtils.processRequestData(data=data, origin="search")
    # Sends search query to Redis
    searchDataResponseCode, searchDataResponseData, searchRequestMsg = redisConnector.searchData(data=processedData)
    # Sets response data
    response_data = requestUtils.processResponse(requestType="search",
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
@app.route("/api/address/modify/update", methods=["POST"])
async def updateAddress():
    permitted_roles = ["admin"]
    # Loads request auth headers
    authContext.authUser(permitted_roles=permitted_roles,
                         auth_data=request.authorization)
    # Loads data from request
    data:bytes = await request.get_data()
    # Loads data from request
    processedData = requestUtils.processRequestData(data=data, origin="update")
    # Updates data in Redis
    updateRecordResponseCode, updateRecordResponseMsg = redisConnector.updateRecord(data=processedData)
    # Sets response data
    response_data = requestUtils.processResponse(requestType="update",
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
@app.route("/api/address/modify/delete", methods=["POST"])
async def deleteAddress():
    permitted_roles = ["admin"]
    # Loads request auth headers
    authContext.authUser(permitted_roles=permitted_roles,
                         auth_data=request.authorization)
    # Loads data from request
    data:bytes = await request.get_data()
    # Loads data from request
    processedData = requestUtils.processRequestData(data=data, origin="delete")
    # Deletes data in Redis
    deleteRecordResponseCode, deleteRecordResponseMsg = redisConnector.deleteRecord(data=processedData)
    # Sets response data
    response_data = requestUtils.processResponse(requestType="delete",
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


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5005, debug=True)
    






