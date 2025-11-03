import mysql.connector
from datetime import datetime

class Database:
    def __init__(self):
        self.connect()

    def connect(self):
        """Establish connection to MySQL"""
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="", #Change this if needed
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

class Request:
    def __init__(self, db):
        self.db = db

    # Create row in Request table
    def createReq(self, reqDescription, helpNeededDate, helpNeededTime, category, userID):
        # Not included columns & reason - requestID (auto-increment PK), reqCreatedOn (DEFAULT CURRENT_DATE), viewCount & shortlistCount (DEFAULT 0), reqStatus (DEFAULT 'Open')

        # Checks that all fields are filled
        if not all([reqDescription, helpNeededDate, helpNeededTime, category, userID]):
            return {"message": "Failed to create request: all fields are required."}
        
        # Checks date and time inputs
        #Assuming date input follows format of DD/MM/YYYY and time input follows 24-hr format HH:MM
        if not self.isDateValid(helpNeededDate):
            return {"message": "Failed to create request: date field incorrectly filled."}
        
        if not self.isTimeValid(helpNeededTime):
            return {"message": "Failed to create request: time field incorrectly filled."}
        
        # Inserts new request
        sql = """INSERT INTO Request
        (reqDescription, helpNeededDate, helpNeededTime, category, userID)
        VALUES (%s, %s, %s, %s, %s)"""
        values = (reqDescription, helpNeededDate, helpNeededTime, category, userID)
        self.db.execute(sql,values)
        return {"message": f"{category} request for {helpNeededDate} at {helpNeededTime} created successfully!"}
    
    def viewReq(self, userID):
        # Receives all requests made by this user from Request table
        sql = """SELECT requestID, reqDescription, reqCreatedOn, helpNeededDate, helpNeededTime, reqStatus, viewCount, shortlistCount, category, userID
        FROM Request
        WHERE userID = %s"""
        values = (userID,)
        return self.db.fetch(sql, values)
    
    def updateReq(self, requestID, reqDescription, helpNeededDate, helpNeededTime, reqStatus, category, userID):
        sql = """UPDATE Request
        SET reqDescription = '%s', helpNeededDate = '%s', helpNeededTime = '%s', reqStatus = '%s', category = '%s'
        WHERE requestID = '%s' AND userID = '%s'"""
        values = (reqDescription, helpNeededDate, helpNeededTime, reqStatus, category, requestID, userID)
        self.db.execute(sql, values)

    def deleteReq(self, requestID, userID):
        sql = """DELETE FROM Request
        WHERE requestID = '%s' AND userID = '%s'"""
        values = (requestID, userID)
        self.db.execute(sql, values)

    def searchReq(self, requestID, userID):
        sql = """SELECT requestID, reqDescription, reqCreatedOn, helpNeededDate, helpNeededTime, reqStatus, viewCount, shortlistCount, category, userID
        FROM Request
        WHERE requestID = '%s' AND userID = '%s'"""
        values = (requestID, userID)
        return self.db.fetch(sql, values)
    
    def reqViewCount(self, userID):
        sql = """SELECT requestID, viewCount
        FROM Request
        WHERE userID = '%s'"""
        values = (userID,)
        return self.db.fetch(sql, values)
    
    def reqShortlistCount(self, userID):
        sql = """"SELECT requestID, shortlistCount
        FROM Request
        WHERE userID = '%s'"""
        values = (userID,)
        return self.db.fetch(sql, values)
    
    def viewCompletedReq(self, userID):
        sql = """SELECT requestID, reqDescription, reqCreatedOn, helpNeededDate, helpNeededTime, reqStatus, viewCount, shortlistCount, category, userID
        FROM Request
        WHERE reqStatus = '%s' AND userID = '%s'"""
        values = ('Completed', userID)
        return self.db.fetch(sql, values)
    
    def searchCompletedReq(self, requestID, userID):
        sql = """SELECT requestID, reqDescription, reqCreatedOn, helpNeededDate, helpNeededTime, reqStatus, viewCount, shortlistCount, category, userID
        FROM Request
        WHERE reqStatus = '%s' AND requestID = '%s' AND userID = '%s'"""
        values = ('Completed', requestID, userID)
        return self.db.fetch(sql, values)
    
    def isDateValid(dateInput):
    # Accepts date input following this format -> DD/MM/YYYY
        try:
            datetime.strptime(dateInput, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def isTimeValid(timeInput):
    # Accepts time input following this format (24 hour format) -> HH:MM
        try:
            datetime.strptime(timeInput, "%H:%M")
            return True
        except ValueError:
            return False