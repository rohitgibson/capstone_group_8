import sqlite3
from typing import Any
from uuid import uuid4

from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from pydantic import ValidationError

from models.db.authModels import User, UserCheck, UserUpdate, UserDelete, Base
from utils.miscUtils import MiscUtils

class AuthConnection:
    # Begin Connection Init Workflow
    def __init__(self):
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
        self.cwd = "./src/app/auth"

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
            self.usersTableCreate(data={"username":"root", "password":"root", "role":"root"})
            self.usersTableCreate(data={"username":"admin", "password":"admin", "role":"admin"})
            self.usersTableCreate(data={"username":"basic", "password":"basic", "role":"basic"})
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

    def usersTableCreate(self, data: dict[str, Any]) -> tuple[int, dict[str, Any], str]:
        try:
            createData = UserCheck(**data).model_dump(mode="JSON")
            username = createData["username"]
            password = createData["password"]
            role = createData["role"]
        except ValidationError as e:
            return 400, {}, f"Add credentials operation failed: {e}"
        except Exception as e:
            return 500, {}, f"Miscellaneous server error: {e}"

        try:
            new_user = User(id=str(uuid4()),
                            username=username,
                            password=generate_password_hash(password=password, method="pbkdf2:sha256"),
                            role=role)
            self.db_session.add(instance=new_user)
            self.db_session.commit()
        except Exception as e:
            self.resetSession()
            return 500, {}, f"Miscellaneous server error: {e}"
        
        return 201, {}, "Credentials successfully created"

    def usersTableRead(self, username:str) -> list[dict[str, Any]]:
        try:
            UserCheck.model_validate({"username": username, "password": "password", "role": "role"})
            read_statement = select(User).where(User.username == username)
            results = [{"id":user.id, "username":user.username, "password":user.password, "role":user.role} for user in self.db_session.scalars(read_statement).all()]
        except Exception as e:
            print("Error occured while trying to read auth users:", e)
            self.resetSession()
            results = []

        return results

    def usersTableUpdate(self, data: dict[str, Any]) -> tuple[int, dict, str]:
        try:
            updateData = UserUpdate(**data).model_dump(mode="JSON")
            username = updateData["username"]
            changes = updateData["changes"]
        except ValidationError as e:
            return 400, {}, f"Update credentials operation failed: {e}"
        except Exception as e:
            return 500, {}, f"Miscellaneous server error: {e}"

        try:
            prev_user = self.usersTableRead(username=username)[0]["id"]
            update_statement = update(User).where(User.id == prev_user).values(username=changes['username'],
                                                                               password=(generate_password_hash(password=changes["password"], method="pbkdf2:sha256")),
                                                                               role=changes["role"])
            self.db_session.execute(update_statement)
            self.db_session.commit()
        except Exception as e:
            self.resetSession()    
            return 500, {}, f"Miscellaneous server error: {e}"

        return 201, {}, "Credentials successfully updated."    

    def usersTableDelete(self, data: dict[str, Any]) -> tuple[int, dict, str]:
        try:
            deleteData = UserDelete(**data).model_dump(mode="JSON")
            username = deleteData["username"]
        except ValidationError as e:
            return 400, {}, f"Delete credentials operation failed: {e}"
        except Exception as e:
            return 500, {}, f"Miscellaneous server error: {e}"

        try:
            prev_user = self.usersTableRead(username=username)[0]["id"]
            delete_statement = delete(User).where(User.id == prev_user)
            self.db_session.execute(delete_statement)
            self.db_session.commit()
        except Exception as e:
            self.resetSession()   
            return 500, {}, f"Miscellaneous server error: {e}"
        
        return 200, {}, "Credentials successfully deleted"

