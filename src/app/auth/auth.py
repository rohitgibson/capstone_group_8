from os import getcwd
from typing import Union
import base64

from quart import abort

from auth.modules.authVerification import AuthVerification

class HTTPBasicAuth():
    def __init__(self):
        self.authVerification = AuthVerification()

    def authUser(self, permitted_roles:list[str], auth_data):
        if auth_data is not None and type(auth_data) == dict:
            auth_data = dict(auth_data)
            role = self.authVerification.checkUserCredentials(username=auth_data["username"], password=auth_data["password"])
        elif auth_data is not None and type(auth_data) == str:
            auth = str(auth_data).split(" ")[1]
            auth_str = base64.b64decode(auth).decode().split(":")
            role = self.authVerification.checkUserCredentials(username=auth_str[0], password=auth_str[1])
        else:
            abort(403)

        if role not in permitted_roles:
            abort(403)
        else:
            pass