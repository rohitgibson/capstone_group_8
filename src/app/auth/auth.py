from os import getcwd
from typing import Union

from quart import abort

from auth.modules.authVerification import AuthVerification

class HTTPBasicAuth(AuthVerification):
    def __init__(self):
        pass

    def authUser(self, permitted_roles:list[str], auth_data):
        if auth_data is not None:
            auth_data = dict(auth_data)
            role = self.checkUserCredentials(username=auth_data["username"], password=auth_data["password"])
        else:
            abort(403)

        if role not in permitted_roles:
            abort(403)
        else:
            pass