import simplejson as json
from flask import Flask, request, make_response, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

from db.redisConnector import RedisConnector
# from auth.authContext import AuthContext
from utils.requestUtils import RequestUtils

app = Flask(__name__)

redisConnector = RedisConnector()

requestUtils = RequestUtils()


# ENDPOINT - add address
@app.route("/api/address/add", methods=["POST"])
def addAddress():
    # Loads data from request
    processedData = requestUtils.processRequestData(data=request.data, origin="add")
    # Adds data to Redis db
    addRecordResponseCode, addRecordResponseMsg = redisConnector.addRecord(data=processedData)
    # Creates response object
    response = make_response('Response')
    # Sets response data
    response.data = requestUtils.processResponse(requestType="add",
                                                 requestData=processedData,
                                                 responseCode=addRecordResponseCode,
                                                 responseMsg=addRecordResponseMsg)
    # Sets response data mimetype
    response.mimetype = "application/json"
    # Sets response HTTP status code
    response.status_code = addRecordResponseCode
    # Returns response object
    return response


# ENDPOINT - search address
@app.route("/api/address/search", methods=["GET"])
def searchAddress():
    # Loads data from request
    processedData = requestUtils.processRequestData(data=request.data, origin="search")
    # Sends search query to Redis
    searchDataResponseCode, searchDataResponseData, searchRequestMsg = redisConnector.searchData(data=processedData)
    # Creates response object
    response = make_response('Response')
    # Sets response HTTP status code
    response.status_code = searchDataResponseCode
    # Sets response data
    response.data = requestUtils.processResponse(requestType="search",
                                                 requestData=searchDataResponseData,
                                                 responseCode=searchDataResponseCode,
                                                 responseMsg=searchRequestMsg)
    # Sets response data mimetype
    response.mimetype = "application/json"
    # Returns response object
    return response


# ENDPOINT - update address
@app.route("/api/address/modify/update", methods=["POST"])
def updateAddress():
    # Loads data from request
    processedData = requestUtils.processRequestData(data=request.data, origin="update")
    # Updates data in Redis
    updateRecordResponseCode, updateRecordResponseMsg = redisConnector.updateRecord(data=processedData)
    # Creates response object
    response = make_response('Response')
    # Sets response data
    response.data = requestUtils.processResponse(requestType="update",
                                                 requestData=processedData,
                                                 responseCode=updateRecordResponseCode,
                                                 responseMsg=updateRecordResponseMsg)
    # Sets response data mimetype
    response.mimetype = "application/json"
    # Sets response HTTP status code
    response.status_code = updateRecordResponseCode

    # Returns response object
    return response


# ENDPOINT - delete address
@app.route("/api/address/modify/delete", methods=["POST"])
def deleteAddress():
    # Loads data from request
    processedData = requestUtils.processRequestData(data=request.data, origin="delete")
    # Deletes data in Redis
    deleteRecordResponseCode, deleteRecordResponseMsg = redisConnector.deleteRecord(data=processedData)
    # Creates response object
    response = make_response('Response')
    # Sets response data
    response.data = requestUtils.processResponse(requestType="delete",
                                                 requestData=processedData,
                                                 responseCode=deleteRecordResponseCode,
                                                 responseMsg=deleteRecordResponseMsg)
    # Sets response data mimetype
    response.mimetype = "application/json"
    # Set response HTTP status code
    response.status_code = deleteRecordResponseCode
    # Returns response object
    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5005, debug=True)
    






