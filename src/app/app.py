import socket
import os

from quart import Quart, Response

from blueprints.address import address_blueprint
from blueprints.users import user_blueprint
from blueprints.demo import demo_blueprint
from utils.requestUtils import RequestUtils

os.environ["APP_VERSION"] = "0.9.0"

app = Quart(__name__)

requestUtils = RequestUtils()

app.register_blueprint(address_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(demo_blueprint)

@app.errorhandler(403)
def forbidden(status_code):
    # Set HTTP response status code
    response_status_code = 403
    # Sets response status message
    response_msg = "Auth credentials not verified or unable to access resource with role permissions."
    # Sets response data
    response_data = requestUtils.processAbortResponse(responseCode=response_status_code, responseMsg=response_msg)
    # Sets response data mimetype
    response_mimetype = "application/json"

    return Response(response=response_data,
                    status=response_status_code,
                    mimetype=response_mimetype), 403

@app.errorhandler(404)
def resourceNotFound(status_code):
    # Set HTTP response status code
    response_status_code = 404
    # Sets response status message
    response_msg = "Resource not found."
    # Sets response data
    response_data = requestUtils.processAbortResponse(responseCode=response_status_code, responseMsg=response_msg)
    # Sets response data mimetype
    response_mimetype = "application/json"

    return Response(response=response_data,
                    status=response_status_code,
                    mimetype=response_mimetype), 404

@app.errorhandler(500)
def internalServerError(status_code):
    # Set HTTP response status code
    response_status_code = 500
    # Sets response status message
    response_msg = "Miscellaneous server error."
    # Sets response data
    response_data = requestUtils.processAbortResponse(responseCode=response_status_code, responseMsg=response_msg)
    # Sets response data mimetype
    response_mimetype = "application/json"

    return Response(response=response_data,
                    status=response_status_code,
                    mimetype=response_mimetype), 500


print("External address:", socket.gethostbyname(socket.gethostname()), "\n", app.url_map)
