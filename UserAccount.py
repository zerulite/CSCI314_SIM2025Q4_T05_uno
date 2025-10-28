import mysql.connector

class Database:
    def __init__(self):
        self.connect()

    def connect(self):
        """Establish connection to MySQL"""
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Splatoon2!", #Change this if needed
                database="csit314"
            )
            self.cursor = self.connection.cursor()
            print("Database connected successfully!")
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")

    def execute(self, query, values=None):
        """Execute an INSERT/UPDATE/DELETE query"""
        self.cursor.execute(query, values or ())
        self.connection.commit()

    def fetch(self, query, values=None):
        """Execute a SELECT query and return results"""
        self.cursor.execute(query, values or ())
        return self.cursor.fetchall()

    def close(self):
        """Close the database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")


class UserAccount:
    def __init__(self):
        self.db = Database()

    #Create Account
    def create_acct(self, userID, password, name, email, profile, userState):
        check_sql = "SELECT * FROM UserAccount WHERE userID = %s"
        if self.db.fetch(check_sql, (userID,)):
            return {"message": f"User {userID} already exists."}
        
        sql = """INSERT INTO UserAccount
                 (userID, password, name, email, profile, userState) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (userID, password, name, email, profile, userState)
        self.db.execute(sql, values)
        self.db.close()
        return {"message": f"User {userID} successfully created."}

    #Update Account
    def update_acct(self, userID, password, name, email, profile, userState):
        check_sql = "SELECT * FROM UserAccount WHERE userID = %s"
        if self.db.fetch(check_sql, (userID,)):
            sql = """UPDATE UserAccount 
                 SET password=%s, name=%s, email=%s, profile=%s, userState=%s 
                 WHERE userID=%s"""
            values = (password, name, email, profile, userState, userID)
            self.db.execute(sql, values)
            self.db.close()
            return {"message": f"User {userID} updated succesfully."}
        else:
            self.db.close()
            return {"message": f"User {userID} update failed."}
