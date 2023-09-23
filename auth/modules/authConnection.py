import mysql.connector as mariadb

class AuthConnection:
    # Begin Connection Init Workflow
    def __init__(self):
        """ Initializes connection with auth credentials database.
        
        
        """
        self.openConnection()
        # self.

        
    def openConnection(self):
        """ Opens connection to auth credentials database
        
        """
        try:
            self.conn = mariadb.connect(
                user="cred_user",
                password="cred_pass",
                host="localhost",
                port=3306,
                database="auth_db"
            )
            self.cursor = self.conn.cursor()
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