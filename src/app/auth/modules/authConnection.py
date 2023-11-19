from os import makedirs
import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.db.authModels import Role, User
from utils.miscUtils import MiscUtils

class AuthConnection:
    # Begin Connection Init Workflow
    def __init__(self, current_working_dir:str):
        """ 
        Creates and initializes connection with the auth credentials database.
        
        
        """
        self.cwd = current_working_dir

        self.miscUtils = MiscUtils()


        self.openConnection()

        
    def openConnection(self):
        """ Opens connection to auth credentials database
        
        """
        

        try:
            self.miscUtils.createPath(rf"{self.cwd}/db")
            
            
        except Exception as e:
            print("Attempted to start auth database connection. Encountered an error:",e)
            exit(1)

    def createUsersTable(self):
        """ Creates a Users table in the database if one doesn't already exist
        
        """
        createTableQuery = """
        CREATE TABLE IF NOT EXISTS USERS (
        username
        )

        """

        pass

    def searchUsersTable(self, username):
        pass