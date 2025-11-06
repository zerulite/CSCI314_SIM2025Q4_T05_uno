import mysql.connector
from datetime import datetime

class Database:
    def __init__(self):
        self.connect()

    def connect(self):
        """Establish connection to MySQL"""
        try:
            self.connection = mysql.connector.connect(
                host="127.0.0.1",
                port=3306,
                user="root",
                password="0000", #Change this if needed
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

    # ============
    # MAIN METHODS
    # ============

    # Create row in Request table
    def createReq(self, reqDescription: str, helpNeededDate: str, helpNeededTime: str, category: str, userID: str):
        # Not included columns & reason - requestID (auto-increment PK), reqCreatedOn (DEFAULT CURRENT_DATE), viewCount & shortlistCount (DEFAULT 0), reqStatus (DEFAULT 'Open')

        # Checks that all fields are filled
        if not all([reqDescription, helpNeededDate, helpNeededTime, category, userID]):
            return {"message": "Failed to create request: all fields are required."}
        
        # Checks date and time inputs
        # Assuming date input follows format of YYYY-MM-DD and time input follows 24-hr format HH:MM
        if not self.isDateValid(helpNeededDate):
            return {"message": "Failed to create request: date field incorrectly filled."}
        
        if not self.isTimeValid(helpNeededTime):
            return {"message": "Failed to create request: time field incorrectly filled."}
        
        # Adjusts the time input to follow MySQL time datatype format
        helpNeededTime = helpNeededTime + ":00"
        
        # Checks category input exists in database
        if not self.isCategoryValid(category):
            return {"message": "Failed to create request: category field incorrectly filled."}
        
        # Inserts new request
        sql = """INSERT INTO Request
        (reqDescription, helpNeededDate, helpNeededTime, category, userID)
        VALUES (%s, %s, %s, %s, %s)"""
        values = (reqDescription, helpNeededDate, helpNeededTime, category, userID)
        self.db.execute(sql,values)
        return {"message": f"Request created successfully: {category} request for {helpNeededDate} at {helpNeededTime}"}
    
    # Returns all requests made by this user from Request table in a list(tuples)
    def viewReq(self, userID: str):
        # Check if any request(s) exists under this user
        if self.doesUserHaveReq(userID):
            sql = """SELECT requestID, reqDescription, reqCreatedOn, helpNeededDate, helpNeededTime, reqStatus, viewCount, shortlistCount, category, userID, volunteer
            FROM Request
            WHERE userID = %s"""
            values = (userID,)
            return self.db.fetch(sql, values)
        else:
            return {"message": "Failed to view request: User does not have any requests."}
    
    # Update a specified request's info from the table
    def updateReq(self, requestID: str, reqDescription: str, helpNeededDate: str, helpNeededTime: str, reqStatus: str, category: str, userID: str):        
        # Checks if requestID was entered and if the requestID/userID exists in the table
        if len(requestID) == 0:
            return {"message": "Failed to update request: requestID field not filled."}
        else:
            # Checks and converts requestID input
            result = self.strToIntConverter(requestID)
            if result:
                requestID = result
            else:
                return {"message": "Failed to update request: requestID field incorrectly filled."}
            
            result = self.doesReqExist(requestID, userID)
            if not (result):
                return {"message": f"Failed to update request: Request #{requestID} not found for user({userID})."}

        # Checks date and time inputs (if entered)
        if len(helpNeededDate) != 0:
            if not self.isDateValid(helpNeededDate):
                return {"message": "Failed to update request: date field incorrectly filled."}
        
        if len(helpNeededTime) != 0:
            if not self.isTimeValid(helpNeededTime):
                return {"message": "Failed to update request: time field incorrectly filled."}
            
        # Adjusts the time input to follow MySQL time datatype format
        helpNeededTime = helpNeededTime + ":00"
            
        # Checks reqStatus input
        if len(reqStatus) != 0:
            result = self.isStatusValid(reqStatus)
            if result:
                reqStatus = result
            else:
                return {"message": "Failed to update request: status field incorrectly filled."}
            
        # Checks category input exists in database
        if not self.isCategoryValid(category):
            return {"message": "Failed to create request: category field incorrectly filled."}
            
        # Filters out empty arguments
        updatesRaw = {"reqDescription": reqDescription, 
                   "helpNeededDate": helpNeededDate, 
                   "helpNeededTime": helpNeededTime, 
                   "reqStatus": reqStatus, 
                   "category": category}
        updatesFiltered = {k: v for k, v in updatesRaw.items() if v != ""}
        if len(updatesFiltered) == 0:
            return {"message": "Failed to update request: nothing to update."}

        # Updates request
        setClause = ", ".join([f"{k} = %s" for k in updatesFiltered])
        sql = f"UPDATE Request SET {setClause} WHERE requestID = %s AND userID = %s"
        values = list(updatesFiltered.values())
        values.extend([requestID, userID])
        self.db.execute(sql, values)
        return {"message": f"Request #{requestID} updated successfully!"}

    # Delete a specified request's info off the table
    def deleteReq(self, requestID: str, userID: str):
        # Checks if requestID was entered and if the requestID/userID exists in the table
        if len(requestID) == 0:
            return {"message": "Failed to delete request: requestID field not filled."}
        else:
            # Checks and converts requestID input
            result = self.strToIntConverter(requestID)
            if result:
                requestID = result
            else:
                return {"message": "Failed to delete request: requestID field incorrectly filled."}
            
            result = self.doesReqExist(requestID, userID)
            if not (result):
                return {"message": f"Failed to delete request: Request #{requestID} not found for user({userID})."}
            
        # Deletes request
        sql = """DELETE FROM Request
        WHERE requestID = %s AND userID = %s"""
        values = (requestID, userID)
        self.db.execute(sql, values)
        return {"message": f"Request #{requestID} deleted successfully!"}

    # Find a specified request's info from the table
    def searchReq(self, requestID: str, userID: str):
        # Checks if requestID was entered and if the requestID/userID exists in the table
        if len(requestID) == 0:
            return {"message": "Failed to find request: requestID field not filled."}
        else:
            # Checks and converts requestID input
            result = self.strToIntConverter(requestID)
            if result:
                requestID = result
            else:
                return {"message": "Failed to find request: requestID field incorrectly filled."}
            
            result = self.doesReqExist(requestID, userID)
            if not (result):
                return {"message": f"Failed to find request: Request #{requestID} not found for user({userID})."}
        
        # Finds request
        sql = """SELECT requestID, reqDescription, reqCreatedOn, helpNeededDate, helpNeededTime, reqStatus, viewCount, shortlistCount, category, userID
        FROM Request
        WHERE requestID = %s AND userID = %s"""
        values = (requestID, userID)
        return self.db.fetch(sql, values)
    
    # Returns nested list of requestID/viewCount tuples of all request associated with userID
    def reqViewCount(self, userID: str):
        # Check if any request(s) exists under this user
        if self.doesUserHaveReq(userID):
            sql = """SELECT requestID, viewCount
            FROM Request
            WHERE userID = %s"""
            values = (userID,)
            return self.db.fetch(sql, values)
        else:
            return {"message": "Failed to view request: User does not have any requests."}
    
    # Returns nested list of requestID/shortlistCount tuples of all request associated with userID
    def reqShortlistCount(self, userID: str):
        # Check if any request(s) exists under this user
        if self.doesUserHaveReq(userID):
            sql = """SELECT requestID, shortlistCount
            FROM Request
            WHERE userID = %s"""
            values = (userID,)
            return self.db.fetch(sql, values)
        else:
            return {"message": "Failed to view request: User does not have any requests."}
    
    # Returns nested list of all requests that have the 'Completed' status associated with userID
    def viewCompletedReq(self, userID: str):    
        sql = """SELECT requestID, reqDescription, reqCreatedOn, helpNeededDate, helpNeededTime, reqStatus, viewCount, shortlistCount, category, userID
        FROM Request
        WHERE reqStatus = %s AND userID = %s"""
        values = ('Completed', userID)
        result = self.db.fetch(sql, values)

        if len(result):
            return result
        else:
            return {"message": "Failed to view request: User does not have any completed requests."}
    
    # Find a specified 'Completed' request's info from the table
    def searchCompletedReq(self, requestID: str, userID: str):
        # Checks if requestID was entered and if the requestID/userID exists in the table
        if len(requestID) == 0:
            return {"message": "Failed to find request: requestID field not filled."}
        else:
            # Checks and converts requestID input
            result = self.strToIntConverter(requestID)
            if result:
                requestID = result
            else:
                return {"message": "Failed to find request: requestID field incorrectly filled."}
            
            result = self.doesReqExist(requestID, userID)
            if not (result):
                return {"message": f"Failed to find request: requestID {requestID} not found for user {userID}."}
        
        # Finds 'Completed' request
        sql = """SELECT requestID, reqDescription, reqCreatedOn, helpNeededDate, helpNeededTime, reqStatus, viewCount, shortlistCount, category, userID
        FROM Request
        WHERE reqStatus = %s AND requestID = %s AND userID = %s"""
        values = ('Completed', requestID, userID)
        result = self.db.fetch(sql, values)

        if len(result):
            return result
        else:
            return {"message": f"Failed to find request: Request #{requestID} is not 'Completed'."}
    

    # ======================
    # PRIVATE HELPER METHODS
    # ====================== 
    
    # Checks if userID has any requests associated with it
    # Returns 0 is none found, returns x (where x > 0) if found; Can be used as 0 = False, x = True
    def doesUserHaveReq(self, userID: str):
        sql = """SELECT * FROM Request WHERE userID = %s"""
        values = (userID,)
        result = self.db.fetch(sql, values)
        return len(result)
    
    # Specifically used for requestID since the table stores it as an int but html takes in as str
    # Returns requestID converted in int if tests pass, False if test fails
    @staticmethod
    def strToIntConverter(requestID: str):
        if requestID.isdigit():
            # Edge case of user entering "0" as requestID and passing the .isdigit() is self-solving as int("0") will return as False
            return int(requestID)
        else:
            return False
    
    # Checks if specified requestID/userID pair has an existing request in the table
    def doesReqExist(self, requestID: int, userID: str):
        sql = "SELECT * FROM Request WHERE requestID = %s AND userID = %s"
        values = (requestID, userID)
        result = self.db.fetch(sql, values)
        if len(result) == 0:
            # Didnt find a matching requestID/userID pair
            return False
        else:
            return True
    
    # Accepts date input following this format -> YYYY-MM-DD
    @staticmethod
    def isDateValid(dateInput: str):
        try:
            datetime.strptime(dateInput, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    # Accepts time input following this format (24 hour format) -> HH:MM
    @staticmethod
    def isTimeValid(timeInput: str):
        try:
            datetime.strptime(timeInput, "%H:%M")
            return True
        except ValueError:
            return False
        
    # Accepts status input according to words in this dict
    # Returns false if not present; returns the word (properly capitalized) if present
    @staticmethod
    def isStatusValid(statusInput: str):
        testChecker = False
        if not statusInput.isalpha():
            return testChecker
        acceptedStatuses = ["Open", "Completed"]
        statusInput = statusInput.capitalize()
        for word in acceptedStatuses:
            if word == statusInput:
                testChecker = word
        return testChecker
    
    def isCategoryValid(self, category: str):
        if not category.isalpha():
            return False
        else:
            category = category.capitalize()
        sql = """SELECT category FROM category"""
        result = self.db.fetch(sql)
        for cat in result:
            if cat[0] == category:
                return True
            
        return False

        # print(result)
    

    # =================
    # INCREMENT METHODS
    # =================

    # Plan: user should not be able to pass anything; loading/pressing 'read more' should automatically call this method thus no return too
    def incViewCount(self, requestID: str, userID: str):
        sql = """UPDATE Request 
        SET viewCount = viewCount + 1 
        WHERE requestID = %s AND userID = %s"""
        values = (requestID, userID)
        self.db.execute(sql, values)

    # Plan: user should not be able to pass anything; pressing 'shortlist' should automatically call this method thus no return too
    def incShortlistCount(self, requestID: str, userID: str):
        sql = """UPDATE Request 
        SET shortlistCount = shortlistCount + 1 
        WHERE requestID = %s AND userID = %s"""
        values = (requestID, userID)
        self.db.execute(sql, values)