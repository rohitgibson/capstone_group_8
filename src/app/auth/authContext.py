from os import getcwd

from auth.modules.authConnection import AuthConnection
from auth.modules.authVerification import AuthVerification

class AuthContext:
    def __init__(self):
        self.authVerification = AuthVerification(current_working_dir=getcwd())