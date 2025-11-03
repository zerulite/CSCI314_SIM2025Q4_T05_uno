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

    def createReq(self, reqDescription, helpNeededDate, helpNeededTime, reqStatus, category, userID):
        # Inserts all required info into Request table
        # Not included columns & reason - requestID (auto-increment PK), reqCreatedOn (DEFAULT CURRENT_DATE), viewCount & shortlistCount (DEFAULT 0)
        sql = """INSERT INTO Request
        (reqDescription, helpNeededDate, helpNeededTime, reqStatus, category, userID)
        VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (reqDescription, helpNeededDate, helpNeededTime, reqStatus, category, userID)
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