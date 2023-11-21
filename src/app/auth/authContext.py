from os import getcwd
from typing import Union

from quart import abort

from auth.modules.authVerification import AuthVerification

class AuthContext:
    def __init__(self):
        self.authVerification = AuthVerification(current_working_dir=f"{getcwd()}/src/app/auth")

    def authUser(self, permitted_roles:list[str], auth_data):
        if auth_data is not None:
            auth_data = dict(auth_data)
            role = self.authVerification.checkUserCredentials(username=auth_data["username"], password=auth_data["password"])
        else:
            abort(403)

        if role not in permitted_roles:
            abort(403)
        else:
            pass