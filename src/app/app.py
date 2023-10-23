from asyncio import get_event_loop

import simplejson as json
from quart import Quart, request, Response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

from db.redisConnector import RedisConnector
# from auth.authContext import AuthContext
from utils.requestUtils import RequestUtils

app = Quart(__name__)


redisConnector = RedisConnector()
requestUtils = RequestUtils()

@app.before_serving
async def startup():
    loop = get_event_loop()
    loop.create_task(redisConnector.healthCheck())

# ENDPOINT - add address
@app.route("/api/address/add", methods=["POST"])
async def addAddress():
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
    






