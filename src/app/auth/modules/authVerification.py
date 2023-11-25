from typing import Union

from werkzeug.security import check_password_hash

from auth.modules.authConnection import AuthConnection

class AuthVerification:
    def __init__(self):
        self.authConnection = AuthConnection()
        self.prev_authd_users = [{"username":"username"}]

    def checkUserCredentials(self, username:str, password:str) -> Union[str, None]:
        """ 
        Executes user credential check workflow
        
        """
        # Checks previously auth'd users for quick match
        user_pass, user_role = self.checkAuthdUsers(username=username)
        # If no match in previously auth'd users, checks auth database
        if None in [user_pass, user_role]:
            user_pass, user_role = self.checkDbUsers(username=username)
            password_valid = self.checkPassword(user_pass=str(user_pass), password=str(password))
        else:
            password_valid = self.checkPassword(user_pass=str(user_pass), password=str(password))
        # Check that the passwords match
        if password_valid is True:
            self.prev_authd_users.append({"username":username, "password":user_pass, "role":user_role})
            return user_role
        else: 
            return None
    
    def checkAuthdUsers(self, username:str) -> Union[tuple[str, str], tuple[None, None]]:
        if self.prev_authd_users == [{}]:
            return None, None
        else:
            pass

        try:
            filter_prev_authd_users = list(filter(lambda user: user["username"] == username, self.prev_authd_users))
        except Exception as e:
            print("Breakpoint 1", e)
            return None, None

        if filter_prev_authd_users != []:
            return filter_prev_authd_users[0]["password"], filter_prev_authd_users[0]["role"]
        else:
            return None, None

    def checkDbUsers(self, username:str) -> Union[tuple[str, str], tuple[None, None]]:
        auth_db_matching_users = self.authConnection.usersTableRead(username=username)

        if auth_db_matching_users != []:
            return auth_db_matching_users[0]["password"], auth_db_matching_users[0]["role"]
        else:
            return None, None

    def checkPassword(self, user_pass:str, password:str) -> bool:
        return check_password_hash(pwhash=user_pass, password=password)