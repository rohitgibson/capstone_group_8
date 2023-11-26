from quart import Blueprint, request, Response

from utils.requestUtils import RequestUtils
from auth.auth import HTTPBasicAuth
from models.api.userModels import UserCheck, Update, Delete

user_blueprint = Blueprint("user", __name__)

auth = HTTPBasicAuth()
requestUtils = RequestUtils()

# ENDPOINT -- ADD AUTH USER
@user_blueprint.route("/api/users/add", methods=["POST"])
async def addUsers():
    permitted_roles = ["root"]
    # Loads request auth headers
    auth.authUser(permitted_roles=permitted_roles,
                  auth_data=rf"{request.authorization}")
    # Loads data from request
    data:bytes = await request.get_data()
    # Converts data to Python dictionary
    processedData = UserCheck(**requestUtils.processRequestData(data=data, origin="user_add")).model_dump(mode="JSON")
    # Adds data to Users table in auth db
    auth.authConnection.usersTableCreate(username=processedData["username"],
                                                  password=processedData["password"],
                                                  role=processedData["role"])
    # Sets response data mimetype
    response_mimetype = "application/json"
    # Sets response HTTP status code
    response_status_code = 201
    # Creates response object
    response = Response(status=response_status_code,
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
    data:bytes = await request.get_data()
    # Converts data to Python dictionary
    processedData = Update(**requestUtils.processRequestData(data=data, origin="user_add")).model_dump(mode="JSON")
    # Adds data to Users table in auth db
    auth.authConnection.usersTableUpdate(username=processedData["username"],
                                         changes=processedData["changes"])
    # Sets response data mimetype
    response_mimetype = "application/json"
    # Sets response HTTP status code
    response_status_code = 201
    # Creates response object
    response = Response(status=response_status_code,
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
    data:bytes = await request.get_data()
    # Converts data to Python dictionary
    processedData = Delete(**requestUtils.processRequestData(data=data, origin="user_add")).model_dump(mode="JSON")
    # Adds data to Users table in auth db
    auth.authConnection.usersTableDelete(username=processedData["username"])
    # Sets response data mimetype
    response_mimetype = "application/json"
    # Sets response HTTP status code
    response_status_code = 201
    # Creates response object
    response = Response(status=response_status_code,
                        mimetype=response_mimetype)
    # Returns response object
    return response