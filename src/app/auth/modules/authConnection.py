import sqlite3
from typing import Any
from uuid import uuid4

from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from models.db.authModels import Role, RoleCheck, User, UserCheck, Base
from utils.miscUtils import MiscUtils

class AuthConnection:
    # Begin Connection Init Workflow
    def __init__(self, current_working_dir:str):
        """ 
        Creates and initializes connection with the auth credentials database.
        
        Args:
            `current_working_dir`:
                A string representing the current working directory for the
                AuthContext class. Used to create a filepath for the auth database.

        Returns:
            None.
        """
        
        # Sets current working directory
        self.cwd = current_working_dir

        # Sets hash for passwords
        self.secret_key = "bruh"

        # Initializes MiscUtils for path creation
        self.miscUtils = MiscUtils()

        # Creates db file (if it doesn't exist) and establishes connection
        self.openConnection()

        # notify auth db ready
        print("AUTH CONNECTION - AuthDB successfully connected...")

    def openConnection(self):
        try:
            self.miscUtils.createPath(rf"{self.cwd}/db")
            temp_conn = sqlite3.connect(rf"{self.cwd}/db/auth.db")
            temp_conn.close()
        except Exception as e:
            print("Attempted to create auth database. Encountered an error:",e)
            exit(1)

        try: 
            db_engine = create_engine(rf"sqlite:///{self.cwd}/db/auth.db")
            Base.metadata.create_all(db_engine)
            self.db_session = Session(db_engine)
            self.usersTableCreate(username="root", password="root", role="admin")
        except Exception as e:
            print("Attempted to connect to auth database. Encountered an error:",e)
            exit(1)

    def resetSession(self):
        try:
            self.db_session.close()
            db_engine = create_engine(rf"sqlite:///{self.cwd}/db/auth.db")
            Base.metadata.create_all(db_engine)
            self.db_session = Session(db_engine)
        except Exception as e:
            print("Exception on auth db session reset:", e)

    
    def rolesTableCreate(self, name:str):
        try:
            RoleCheck.model_validate({"name": name})
            new_role = Role(name=name)

            self.db_session.add(instance=new_role)
            self.db_session.commit()
        except Exception as e:
            print("Error on auth db role creation operation.")
            self.resetSession()

    def rolesTableDelete(self, name:str):
        try:
            RoleCheck.model_validate({"name": name})
            delete_statement = delete(Role).where(Role.name == name)

            self.db_session.execute(delete_statement)
            self.db_session.commit()
        except Exception as e:
            print("Error on auth db role deletion operation.")
            self.resetSession()

    def usersTableCreate(self, username:str, password:str, role:str):
        try:
            UserCheck.model_validate({"username": username, "password": password, "role": role})
            new_user = User(id=str(uuid4()),
                            username=username,
                            password=generate_password_hash(password=password),
                            role=role)
            
            self.db_session.add(instance=new_user)
            self.db_session.commit()
        except Exception as e:
            print("Error on auth user creation.")
            self.resetSession()

    def usersTableRead(self, username:str) -> list[dict[str, Any]]:
        try:
            UserCheck.model_validate({"username": username, "password": "password", "role": "role"})
            read_statement = select(User).where(User.username == username)
            results = [{"username":user.username, "password":user.password, "role":user.role} for user in self.db_session.scalars(read_statement).all()]
        except Exception as e:
            print("Error occured while trying to read auth users:", e)
            self.resetSession()
            results = []

        return results

    def usersTableUpdate(self, username:str, changes:dict[str, Any]) -> None:
        print(username, changes)
        try:
            update_statement = update(User).where(User.username == username).values(username=changes['username'],
                                                                                    password=generate_password_hash(password=changes["password"]),
                                                                                    role=changes["role"])
            print(update_statement)
            self.db_session.execute(update_statement)
            self.db_session.commit()
        except Exception as e:
            print("Error occured when updating user records in auth db:", e)
            self.resetSession()        

    def usersTableDelete(self, username:str):
        print(username)
        try:
            delete_statement = delete(User).where(User.username == username)
            print(delete_statement)
            self.db_session.execute(delete_statement)
            self.db_session.commit()
        except Exception as e:
            print("Error occured when deleting user records in auth db:", e)
            self.resetSession()   

