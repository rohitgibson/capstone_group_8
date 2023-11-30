from quart import Blueprint, request, Response

from utils.requestUtils import RequestUtils
from auth.auth import HTTPBasicAuth
from models.db.authModels import UserCheck, UserUpdate, UserDelete

user_blueprint = Blueprint("user", __name__)

auth = HTTPBasicAuth()
requestUtils = RequestUtils()

# ENDPOINT -- ADD AUTH USER
@user_blueprint.route("/api/users/create", methods=["POST"])
async def addUsers():
    permitted_roles = ["root"]
    # Loads request auth headers
    auth.authUser(permitted_roles=permitted_roles,
                  auth_data=rf"{request.authorization}")
    # Loads data from request
    data_nonjson:bytes = await request.get_data()
    data_json:bytes = await request.get_json()
    # Converts data to Python dictionary
    processedData = requestUtils.processRequestData(data_nonjson=data_nonjson, data_json=data_json, origin="add_user")
    # Adds data to Users table in auth db
    response_status_code, response_data, response_msg = auth.authVerification.authConnection.usersTableCreate(data=processedData)
    # Sets response data
    response_data = requestUtils.processResponse(requestType="add_user",
                                                 requestData=processedData,
                                                 responseCode=response_status_code,
                                                 responseMsg=response_msg,
                                                 responseData=None)
    # Sets response data mimetype
    response_mimetype = "application/json"
    # Sets response HTTP status code
    response_status_code = response_status_code
    # Creates response object
    response = Response(response=response_data,
                        status=response_status_code,
                        mimetype=response_mimetype)
    # Returns response object
    return response

@user_blueprint.route("/api/users/update", methods=["POST"])
async def updateUsers():
    permitted_roles = ["root"]
    # Loads request auth headers
    auth.authUser(permitted_roles=permitted_roles,
                  auth_data=rf"{request.authorization}")
    # Loads data from request
    data_nonjson:bytes = await request.get_data()
    data_json:bytes = await request.get_json()
    # Converts data to Python dictionary
    processedData = requestUtils.processRequestData(data_nonjson=data_nonjson, data_json=data_json, origin="update_user")
    # Updates data in Users table in auth db
    response_status_code, response_data, response_msg = auth.authVerification.authConnection.usersTableUpdate(data=processedData)
    # Sets response data
    response_data = requestUtils.processResponse(requestType="update_user",
                                                 requestData=processedData,
                                                 responseCode=response_status_code,
                                                 responseMsg=response_msg,
                                                 responseData=None)
    # Sets response data mimetype
    response_mimetype = "application/json"
    # Creates response object
    response = Response(response=response_data,
                        status=response_status_code,
                        mimetype=response_mimetype)
    # Returns response object
    return response

@user_blueprint.route("/api/users/delete", methods=["POST"])
async def deleteUsers():
    permitted_roles = ["root"]
    # Loads request auth headers
    auth.authUser(permitted_roles=permitted_roles,
                  auth_data=rf"{request.authorization}")
    # Loads data from request
    data_nonjson:bytes = await request.get_data()
    data_json:bytes = await request.get_json()
    # Converts data to Python dictionary
    processedData = requestUtils.processRequestData(data_nonjson=data_nonjson, data_json=data_json, origin="delete_address")
    # Deletes data from Users table in auth db
    response_status_code, response_data, response_msg = auth.authVerification.authConnection.usersTableDelete(data=processedData)
    # Sets response data
    response_data = requestUtils.processResponse(requestType="delete_user",
                                                 requestData=processedData,
                                                 responseCode=response_status_code,
                                                 responseMsg=response_msg,
                                                 responseData=None)
    # Sets response data mimetype
    response_mimetype = "application/json"
    # Creates response object
    response = Response(response=response_data,
                        status=response_status_code,
                        mimetype=response_mimetype)
    # Returns response object
    return response