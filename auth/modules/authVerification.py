from typing import Union

from werkzeug.security import check_password_hash

from auth.modules.authConnection import AuthConnection

class AuthCheckUserCredentials():
    def __init__(self):
        pass

    def checkUserCredentials(self, username, password) -> Union[str, None]:
        """ Executes user credential check workflow
        
        """
        # Checks previously auth'd users for quick match
        
        # If no match in previously auth'd users, checks

        return ""
    
    def checkAuthedUsers(self, username) -> Union[str, None]:


        pass

    def checkDbUsers(self, username, password) -> Union[str, None]:


        pass

    def checkPassword(self, password) -> bool:


        return False

class AuthCheckUserRole():
    def __init__(self):
        pass

    def checkUserRole(self, username:str, storedCredentials:dict) -> Union[str, None]:
        if username in list(storedCredentials.keys()):
            role = storedCredentials["username"]
        else:
            role = None

        return role

class AuthVerification(AuthCheckUserCredentials, AuthCheckUserRole):
    def __init__(self):
        self.storedCredentials = {}

    def verifyUserCredentials(self, username, password):
        user = self.checkUserCredentials(username=username,password=password)

        return user

    def verifyUserRole(self, username:str):
        role = self.checkUserRole(username=username, storedCredentials=self.storedCredentials)

        return role