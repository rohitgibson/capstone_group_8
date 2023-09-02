from flask import Flask, request, Response, jsonify

from connections.redisConnector import RedisConnector

app = Flask(__name__)

redisConnector = RedisConnector()


# ENDPOINT - add address
@app.route("/api/address/add", methods=["POST"])
def addAddress():
    # Loads data from request
    data = request.data
    # Adds data to Redis db
    addRecordResponseCode = redisConnector.addRecord(data=data)
    # Creates response object
    response = Response(status=addRecordResponseCode)
    # Returns response object
    return response


# ENDPOINT - search address
@app.route("/api/address/search", methods=["GET"])
def searchAddress():
    # Loads data from request
    data = request.data
    # Sends search query to Redis
    searchDataResponseCode, searchDataResponseData = redisConnector.searchData(data=data)
    # Creates response object
    response = Response(response=jsonify(searchDataResponseData), status=searchDataResponseCode)
    # Returns response object
    return response


# ENDPOINT - update address
@app.route("/api/address/modify/update", methods=["POST"])
def updateAddress():
    # Loads data from request
    data = request.data
    # Updates data in Redis
    updateRecordResponseCode = redisConnector.updateRecord(data=data)
    # Creates response object
    response = Response(status=updateRecordResponseCode)
    # Returns response object
    return response


# ENDPOINT - delete address
@app.route("/api/address/modify/delete", methods=["POST"])
def deleteAddress():
    pass


# update_dict = {
#     "key": "address:fc452f31-cde2-4518-80df-bbce8d34adef",
#     "data": {
#         "firstName": "John",
#         "lastName": "Dow",
#         "addressLine1": "2300 Windy Ridge",
#         "addressLine2": "",
#         "city": "Atlanta",
#         "stateProv": "ID",
#         "postalCode": "30339",
#         "country": "US"
#     }
# }

# search_dict = {
#     "addressLine1": "2300 Windy Ridge",
#     "addressLine2": "",
#     "city": "Atlanta",
#     "stateProv": "GA",
#     "postalCode": "30339",
#     "country": "US"
# }

# redisConnector.addData(test_dict)
# redisConnector.updateRecord(data=update_dict)
# print("Searching")
# searchData = redisConnector.searchData(data=search_dict)
# print(searchData)








