from quart import Blueprint, request, Response
import pandas as pd

from db.redisConnector import RedisConnector
from auth.auth import HTTPBasicAuth
from utils.requestUtils import RequestUtils
# from models.api.demoModels import 

demo_blueprint = Blueprint("demo", __name__)

redisConnector = RedisConnector()
auth = HTTPBasicAuth()
requestUtils = RequestUtils()

# API routes for restoring database state to 

@demo_blueprint.route("/api/demo/resetdb", methods=["POST"])
async def resetDb():
    permitted_roles = ["root"]
    # Loads request auth headers
    auth.authUser(permitted_roles=permitted_roles,
                  auth_data=rf"{request.authorization}")
    # Wipes all data currently in Redis
    deleteRecordResponseCode, deleteRecordResponseMsg = redisConnector.deleteAllRecords()
    # Read data to list with Pandas
    processedData = pd.read_excel("static/project_2_addresses.xlsx").to_dict(orient="records")
    # Adds data to Redis db
    addRecordResponseCode, addRecordResponseMsg = redisConnector.bulkAddRecord(bulkData=processedData)
    # Sets response data mimetype
    response_mimetype = "application/json"
    # Sets response HTTP status code
    response_status_code = addRecordResponseCode
    # Creates response object
    response = Response(status=response_status_code,
                        mimetype=response_mimetype)
    # Returns response object
    return response

@demo_blueprint.route("/api/demo/deleteallkeys", methods=["POST"])
async def deleteAllKeys():
    permitted_roles = ["root"]
    # Loads request auth headers
    auth.authUser(permitted_roles=permitted_roles,
                  auth_data=rf"{request.authorization}")
    # Wipes all data currently in Redis
    deleteRecordResponseCode, deleteRecordResponseMsg = redisConnector.deleteAllRecords()
    # Sets response data mimetype
    response_mimetype = "application/json"
    # Sets response HTTP status code
    response_status_code = deleteRecordResponseCode
    # Creates response object
    response = Response(status=response_status_code,
                        mimetype=response_mimetype)
    # Returns response object
    return response

@demo_blueprint.route("/api/demo/set-flag/<flag>/<value>", methods=["POST"])
async def setVerboseFlag(flag:str, value:bool):
    permitted_roles = ["root"]
    # Loads request auth headers
    auth.authUser(permitted_roles=permitted_roles,
                  auth_data=rf"{request.authorization}")
    # Sets flag to value
    requestUtils.setCurrentFlags(flag=flag, flag_value=value)
    # Sets response data mimetype
    response_mimetype = "application/json"
    # Sets response HTTP status code
    response_status_code = 200
    # Creates response object
    response = Response(status=response_status_code,
                        mimetype=response_mimetype)
    # Returns response object
    return response