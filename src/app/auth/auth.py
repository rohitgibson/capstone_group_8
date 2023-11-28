from os import getcwd
from typing import Union
import base64

from quart import abort

from auth.modules.authVerification import AuthVerification

class HTTPBasicAuth():
    """
    Authenticates inbound requests using HTTP Basic Auth.
    """

    def __init__(self):
        """
        Initializes the HTTPBasicAuth class.
        """
        self.authVerification = AuthVerification()

    def authUser(self, permitted_roles:list[str], auth_data):
        """
        Verifies the user's credentials and checks whether they're
        authorized to access a resource.

        Args:
            `permitted_roles`: 
                A list of allowed roles for accessing the protected resource.
            `auth_data`: 
                User's authentication data, either as a dictionary or 
                Base64-encoded string.
        """
        try:
            # Check if auth_data is a dictionary with username and password
            if auth_data is not None and type(auth_data) == dict:
                auth_data = dict(auth_data)
                role = self.authVerification.checkUserCredentials(username=auth_data["username"], password=auth_data["password"])

            # Check if auth_data is a Base64-encoded string with username and password
            elif auth_data is not None and type(auth_data) == str:
                auth = str(auth_data).split(" ")[1]
                auth_str = base64.b64decode(auth).decode().split(":")
                role = self.authVerification.checkUserCredentials(username=auth_str[0], password=auth_str[1])

            # If auth_data can't be parsed, raise an abort signal
            else:
                abort(403)

            # Check if the user's role is in the permitted_roles list
            if role not in permitted_roles:
                abort(403)
            else:
                pass

        # If any exception occurs during verification, raise an abort signal
        except Exception:
            abort(403)