import simplejson as json
from flask import Flask, request, make_response, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

from db.redisConnector import RedisConnector
# from auth.authContext import AuthContext
from utils.requestUtils import RequestUtils

app = Flask(__name__)

# auth = HTTPBasicAuth()
# authContext = AuthContext()

redisConnector = RedisConnector()

requestUtils = RequestUtils()

# @auth.verify_password
# def verifyPassword(username, password):
#     user = authContext.verifyUserCredentials(username=username, password=password)
    
#     return user

# @auth.get_user_roles
# def getUserRoles(username):
#     role = authContext.verifyUserRole(username=username)
    
#     return role


# ENDPOINT - add address
@app.route("/api/address/add", methods=["POST"])
def addAddress():
    # Loads data from request
    processedData = requestUtils.processRequestData(data=request.data)
    # Adds data to Redis db
    addRecordResponseCode = redisConnector.addRecord(data=processedData)
    # Creates response object
    response = make_response('Response')
    # Sets response HTTP status code
    response.status_code = addRecordResponseCode
    # Returns response object
    return response


# ENDPOINT - search address
@app.route("/api/address/search", methods=["GET"])
def searchAddress():
    # Loads data from request
    processedData = requestUtils.processRequestData(data=request.data)
    # Sends search query to Redis
    searchDataResponseCode, searchDataResponseData = redisConnector.searchData(data=processedData)
    # Creates response object
    response = make_response('Response')
    # Sets response HTTP status code
    response.status_code = searchDataResponseCode
    # Sets response data
    response.data = searchDataResponseData
    # Sets response data mimetype
    response.mimetype = "application/json"
    # Returns response object
    return response


# ENDPOINT - update address
@app.route("/api/address/modify/update", methods=["POST"])
def updateAddress():
    # Loads data from request
    processedData = requestUtils.processRequestData(data=request.data)
    # Updates data in Redis
    updateRecordResponseCode = redisConnector.updateRecord(data=processedData)
    # Creates response object
    response = make_response('Response')
    # Sets response HTTP status code
    response.status_code = updateRecordResponseCode
    # Returns response object
    return response


# ENDPOINT - delete address
@app.route("/api/address/modify/delete", methods=["POST"])
def deleteAddress():
    # Loads data from request
    processedData = requestUtils.processRequestData(data=request.data)
    # Deletes data in Redis
    deleteRecordResponseCode = redisConnector.deleteRecord(data=processedData)
    # Creates response object
    response = make_response('Response')
    # Set response HTTP status code
    response.status_code = deleteRecordResponseCode
    # Returns response object
    return response

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5005, debug=True)
    






