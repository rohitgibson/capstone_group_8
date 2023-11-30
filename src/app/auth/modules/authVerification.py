from typing import Union

from werkzeug.security import check_password_hash

from auth.modules.authConnection import AuthConnection

class AuthVerification:
    def __init__(self):
        self.authConnection = AuthConnection()

    def checkUserCredentials(self, username:str, password:str) -> Union[str, None]:
        """ 
        Executes user credential check workflow
        """
        # Checks auth database
        user_pass, user_role = self.checkDbUsers(username=username)
        password_valid = self.checkPassword(user_pass=str(user_pass), password=str(password))
        # Check that the passwords match
        if password_valid is True:
            return user_role
        else: 
            return None

    def checkDbUsers(self, username:str) -> Union[tuple[str, str], tuple[None, None]]:
        auth_db_matching_users = self.authConnection.usersTableRead(username=username)

        if auth_db_matching_users != []:
            return auth_db_matching_users[0]["password"], auth_db_matching_users[0]["role"]
        else:
            return None, None

    def checkPassword(self, user_pass:str, password:str) -> bool:
        return check_password_hash(pwhash=user_pass, password=password)