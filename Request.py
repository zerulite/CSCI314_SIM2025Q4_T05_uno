import mysql.connector
from datetime import datetime
from mysql.connector import Error

class Database:
    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host="127.0.0.1",
                port=3306,
                user="root",
                password="Splatoon2!",  
                database="csit314",
                autocommit=True,         
            )
            print("DB: connected (autocommit ON)")
        except Error as err:
            print(f"DB error: {err}")
            self.connection = None

    def ensureConn(self):
        if self.connection is None or not self.connection.is_connected():
            self.connect()

    def execute(self, query, values=None):
        self.ensureConn()
        cur = self.connection.cursor()
        try:
            cur.execute(query, values or ())
            return cur.rowcount
        finally:
            cur.close()

    def fetch(self, query, values=None):
        self.ensureConn()
        cur = self.connection.cursor()
        try:
            cur.execute(query, values or ())
            return cur.fetchall()
        finally:
            cur.close()

    def close(self):
        try:
            if self.connection and self.connection.is_connected():
                self.connection.close()
        except Exception:
            pass

class Request:
    def __init__(self):
        self.db = Database()

    # ============
    # MAIN METHODS
    # ============

    # Create row in Request table
    def createReq(self, reqDescription: str, helpNeededDate: str, helpNeededTime: str, category: str, userID: str):
        # Not included columns & reason - requestID (auto-increment PK), viewCount & shortlistCount (DEFAULT 0), reqStatus (DEFAULT 'Open')

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
            # * covers requestID, reqDescription, helpNeededDate, helpNeededTime, reqStatus, viewCount, shortlistCount, category, userID, volunteer    
            sql = """SELECT * 
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
    def viewAReq(self, requestID: str, userID: str):
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
        # * covers requestID, reqDescription, helpNeededDate, helpNeededTime, reqStatus, viewCount, shortlistCount, category, userID, volunteer    
        sql = """SELECT *
        FROM Request
        WHERE requestID = %s AND userID = %s"""
        values = (requestID, userID)
        return self.db.fetch(sql, values)
    
    def searchReq(self, **kwargs):
    # Remove empty values
        searchFields = {k: v for k, v in kwargs.items() if v}

        # Return message if nothing to search
        if not searchFields:
            return {"message": "Failed to find a request: all fields empty."}

        # Base query
        query = "SELECT * FROM Request WHERE 1=1"
        params = []

        # Fields to check
        for field in ['requestID', 'reqDescription', 'helpNeededDate', 'helpNeededTime', 'category', 'userID']:
            value = searchFields.get(field)
            if value:
                if field in ['reqDescription', 'category']:
                    query += f" AND {field} LIKE %s"
                    params.append(f"%{value}%")
                else:
                    query += f" AND {field} = %s"
                    params.append(value)

        # Execute query
        result = self.db.fetch(query, params)

        if result:
            return result
        else:
            return {"message": "Failed to find a request: no matching request found."}

    
    # def searchReq(self, **kwargs):
        # # Remove empty values
        # search_fields = {k: v for k, v in kwargs.items() if v}

        # # Return empty list if nothing to search
        # if not search_fields:
        #     return {"message": "Failed to find a request: all fields empty."}

        # query = "SELECT * FROM Request WHERE 1=1"
        # params = []

        # for field in ['reqDescription', 'helpNeededDate', 'helpNeededTime', 'category']:
        #     value = search_fields.get(field)
        #     if value:
        #         if field in ['reqDescription', 'category']:
        #             query += f" AND {field} LIKE %s"
        #             params.append(f"%{value}%")
        #         else:
        #             query += f" AND {field} = %s"
        #             params.append(value)

        # result = self.db.fetch(query, params)

        # if len(result):
        #     return result
        # else:
        #     return {"message": "Failed to find a request: no matching request found."}
    
    # Returns nested list of requestID/viewCount tuples of all request associated with userID
    def reqViewCount(self, userID: str):
        # Check if any request(s) exists under this user
        if self.doesUserHaveReq(userID):
            sql = """SELECT *
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
            sql = """SELECT *
            FROM Request
            WHERE userID = %s"""
            values = (userID,)
            return self.db.fetch(sql, values)
        else:
            return {"message": "Failed to view request: User does not have any requests."}
    
    # Returns nested list of all requests that have the 'Completed' status associated with userID
    def viewCompletedReq(self, userID: str):
        # * covers requestID, reqDescription, helpNeededDate, helpNeededTime, reqStatus, viewCount, shortlistCount, category, userID, volunteer    
        sql = """SELECT * 
        FROM Request
        WHERE reqStatus = %s AND userID = %s"""
        values = ('Completed', userID)
        result = self.db.fetch(sql, values)

        if len(result):
            return result
        else:
            return {"message": "Failed to view request: User does not have any completed requests."}
        
    def searchCompletedReq(self, **kwargs):
    # Remove empty values
        searchFields = {k: v for k, v in kwargs.items() if v}

        # Return message if nothing to search
        if not searchFields:
            return {"message": "Failed to find a request: all fields empty."}

        # Base query
        query = "SELECT * FROM Request WHERE reqStatus = 'Completed'"
        params = []

        # Fields to check
        for field in ['requestID', 'reqDescription', 'helpNeededDate', 'helpNeededTime', 'category', 'userID']:
            value = searchFields.get(field)
            if value:
                if field in ['reqDescription', 'category']:
                    query += f" AND {field} LIKE %s"
                    params.append(f"%{value}%")
                else:
                    query += f" AND {field} = %s"
                    params.append(value)

        # Execute query
        result = self.db.fetch(query, params)

        if result:
            return result
        else:
            return {"message": "Failed to find a request: no matching request found."}
    
    # Find a specified 'Completed' request's info from the table
    # def searchCompletedReq(self, requestID: str, userID: str):
    #     # Checks if requestID was entered and if the requestID/userID exists in the table
    #     if len(requestID) == 0:
    #         return {"message": "Failed to find request: requestID field not filled."}
    #     else:
    #         # Checks and converts requestID input
    #         result = self.strToIntConverter(requestID)
    #         if result:
    #             requestID = result
    #         else:
    #             return {"message": "Failed to find request: requestID field incorrectly filled."}
            
    #         result = self.doesReqExist(requestID, userID)
    #         if not (result):
    #             return {"message": f"Failed to find request: requestID {requestID} not found for user {userID}."}
        
    #     # Finds 'Completed' request
    #     # * covers: requestID, reqDescription, helpNeededDate, helpNeededTime, reqStatus, viewCount, shortlistCount, category, userID, volunteer
    #     sql = """SELECT * 
    #     FROM Request
    #     WHERE reqStatus = %s AND requestID = %s AND userID = %s"""
    #     values = ('Completed', requestID, userID)
    #     result = self.db.fetch(sql, values)

    #     if len(result):
    #         return result
    #     else:
    #         return {"message": f"Failed to find request: Request #{requestID} is not 'Completed'."}
    

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

    def getCategories(self):
        sql = """SELECT category FROM category"""
        result = self.db.fetch(sql)
        return result
    

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
    
    #Search New Requests
    def search_new_request(self, **kwargs):
        base = (
            "SELECT r.requestID, r.reqDescription, r.volunteer, r.helpNeededDate, TIME_FORMAT(r.helpNeededTime, '%H:%i') AS helpNeededTime, r.category, r.userID, r.reqStatus "
            "FROM `Request` r "
            "LEFT JOIN `UserAccount` u ON u.userID = r.userID "
            "WHERE r.reqStatus = 'Open'"
        )
        params = []

        for field in ["requestID", "reqDescription", "volunteer", "helpNeededDate", "helpNeededTime", "category", "userID"]:
            value = kwargs.get(field)
            if value not in (None, ""):
                if field in ["reqDescription", "volunteer", "category", "userID"]:
                    base += f" AND r.{field} LIKE %s"
                    params.append(f"%{value}%")
                else:
                    base += f" AND r.{field} = %s"
                    params.append(value)

        limit = int(kwargs.get("limit", 50))
        offset = int(kwargs.get("offset", 0))
        sql = f"{base} LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        rows = self.db.fetch(sql, params)
        print("RESULTS:", len(rows))
        return rows

    #View Individual Request
    def view_individual_request(self, request_id: str):
        sql = (
            "SELECT r.requestID, r.reqDescription, r.volunteer, r.helpNeededDate, TIME_FORMAT(r.helpNeededTime, '%H:%i') AS helpNeededTime, r.category, r.userID, r.reqStatus "
            "FROM `Request` r WHERE r.requestID = %s LIMIT 1"
        )
        return self.db.fetch(sql, (str(request_id),))

    #View All Requests
    def view_all_requests(self, limit=100, offset=0):
        sql = (
            "SELECT r.requestID, r.reqDescription, r.volunteer, r.helpNeededDate, TIME_FORMAT(r.helpNeededTime, '%H:%i') AS helpNeededTime, r.category, r.userID, r.reqStatus "
            "FROM `Request` r "
            "ORDER BY r.helpNeededDate, r.helpNeededTime, r.requestID "
            "LIMIT %s OFFSET %s"
        )
        return self.db.fetch(sql, (int(limit), int(offset)))
    
    #Shortlist Requests
    def add_to_shortlist(self, request_id: str, csr_user_id: str) -> bool:
        sql = """
            INSERT IGNORE INTO RequestShortlist (requestID, userID)
            VALUES (%s, %s)
        """
        params = (str(request_id), str(csr_user_id))
        affected = self.db.execute(sql, params)
        return affected > 0
    
    def shortlist_status(self, request_id: str, csr_user_id: str) -> str:
        try:
            affected = self.db.execute(
                "INSERT IGNORE INTO RequestShortlist (requestID, userID) VALUES (%s, %s)",
                (str(request_id), str(csr_user_id))
            )
            if affected == 1:
                return "added"

            exists = self.db.fetch(
                "SELECT 1 FROM RequestShortlist WHERE requestID=%s AND userID=%s LIMIT 1",
                (str(request_id), str(csr_user_id))
            )
            return "exists" if exists else "error"
        except Exception:
            return "error"

    #Search Shorlist Requests
    def search_shortlisted(
        self,
        csr_user_id,
        requestID=None,
        request=None,
        volunteer=None,
        date=None,
        time=None,
        category=None,
        userID=None,
        completed=None,
        limit: int = 50,
        offset: int = 0,
    ):
        sql = [
            "SELECT r.requestID, r.reqDescription, r.volunteer, r.helpNeededDate, TIME_FORMAT(r.helpNeededTime, '%H:%i') AS helpNeededTime, r.category, r.userID, r.reqStatus",
            "FROM Request r",
            "INNER JOIN RequestShortlist s ON s.requestID = r.requestID",
            "WHERE s.userID = %s",
        ]
        params = [csr_user_id]

        if requestID:
            sql.append("AND r.requestID = %s")
            params.append(requestID)

        if request not in (None, ""):
            sql.append("AND r.reqDescription LIKE %s")
            params.append(f"%{request}%")

        if volunteer not in (None, ""):
            sql.append("AND r.volunteer LIKE %s")
            params.append(f"%{volunteer}%")

        if date:
            sql.append("AND r.helpNeededDate = %s")
            params.append(date)

        if time:
            sql.append("AND r.helpNeededTime = %s")
            params.append(time)

        if category not in (None, ""):
            sql.append("AND r.category LIKE %s")
            params.append(f"%{category}%")

        if userID not in (None, ""):
            sql.append("AND r.userID LIKE %s")
            params.append(f"%{userID}%")

        if completed is not None:
            sql.append("AND (r.reqStatus = %s OR (r.reqStatus IS NULL AND %s = ''))")
            params.extend([completed, completed])

        sql.append("ORDER BY r.requestID LIMIT %s OFFSET %s")
        params.extend([int(limit), int(offset)])

        return self.db.fetch(" ".join(sql), tuple(params))
    
    #View Shortlisted Requests
    def view_shortlist(self, csr_user_id: str, limit=100, offset=0):
        sql = (
            "SELECT r.requestID, r.reqDescription, r.volunteer, r.helpNeededDate, TIME_FORMAT(r.helpNeededTime, '%H:%i') AS helpNeededTime, r.category, r.userID, r.reqStatus "
            "FROM `Request` r "
            "INNER JOIN `RequestShortlist` s ON s.requestID = r.requestID "
            "WHERE s.userID = %s "
            "ORDER BY r.helpNeededDate, r.helpNeededTime, r.requestID "
            "LIMIT %s OFFSET %s"
        )
        return self.db.fetch(sql, (csr_user_id, int(limit), int(offset)))
    
    #Search History
    def search_history(self, **kwargs):
        base = (
            "SELECT r.requestID, r.reqDescription, r.volunteer, r.helpNeededDate, TIME_FORMAT(r.helpNeededTime, '%H:%i') AS helpNeededTime, r.category, r.userID, r.reqStatus "
            "FROM `Request` r "
            "LEFT JOIN `UserAccount` u ON u.userID = r.userID "
            "WHERE 1=1"
        )
        params = []
        base += " AND r.reqStatus = %s"
        params.append("Completed")

        for field in ["requestID", "reqDescription", "volunteer", "helpNeededDate", "helpNeededTime", "category", "userID"]:
            value = kwargs.get(field)
            if value not in (None, ""):
                if field in ["reqDescription", "volunteer", "category", "userID"]:
                    base += f" AND r.{field} LIKE %s"
                    params.append(f"%{value}%")
                else:
                    base += f" AND r.{field} = %s"
                    params.append(value)

        limit = int(kwargs.get("limit", 50))
        offset = int(kwargs.get("offset", 0))
        sql = f"{base} LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        return self.db.fetch(sql, params)
    
    #View History
    def view_history(self, limit=100, offset=0):
        sql = (
            "SELECT r.requestID, r.reqDescription, r.volunteer, r.helpNeededDate, TIME_FORMAT(r.helpNeededTime, '%H:%i') AS helpNeededTime, r.category, r.userID, r.reqStatus "
            "FROM `Request` r "
            "WHERE r.reqStatus = %s "
            "ORDER BY r.helpNeededDate, r.helpNeededTime, r.requestID "
            "LIMIT %s OFFSET %s"
        )
        return self.db.fetch(sql, ("Completed", int(limit), int(offset)))
    # Generate report by date
    def get_requests_by_date(self, date):
        query = """
        SELECT 
            r.requestID, 
            r.reqDescription, 
            r.volunteer,
            r.helpNeededDate, 
            TIME_FORMAT(r.helpNeededTime, '%H:%i') AS helpNeededTime, 
            c.category AS category_name,
            u.name AS user_name, 
            r.reqStatus
        FROM Request r
        LEFT JOIN Category c ON r.category = c.category
        LEFT JOIN UserAccount u ON r.userID = u.userID
        WHERE r.helpNeededDate = %s
        ORDER BY r.helpNeededTime ASC
        """
        results = self.db.fetch(query, (date,))
        return [
            {
                "Request ID": r[0],
                "Description": r[1],
                "Volunteer": r[2] if r[2] else "—",  # show dash if no volunteer assigned
                "Date": r[3].strftime("%Y-%m-%d") if r[3] else "",
                "Time": r[4] if r[4] else "",
                "Category": r[5],
                "User": r[6],
                "Status": r[7]
            }
            for r in results
        ]

    # Generate report by week
    def get_requests_by_week(self, week_start):
        query = """
        SELECT 
            r.requestID, 
            r.reqDescription, 
            r.volunteer,
            r.helpNeededDate, 
            TIME_FORMAT(r.helpNeededTime, '%H:%i') AS helpNeededTime, 
            c.category AS category_name,
            u.name AS user_name, 
            r.reqStatus
        FROM Request r
        LEFT JOIN Category c ON r.category = c.category
        LEFT JOIN UserAccount u ON r.userID = u.userID
        WHERE r.helpNeededDate BETWEEN %s AND DATE_ADD(%s, INTERVAL 6 DAY)
        ORDER BY r.helpNeededDate, r.helpNeededTime ASC
        """
        results = self.db.fetch(query, (week_start, week_start))
        return [
            {
                "Request ID": r[0],
                "Description": r[1],
                "Volunteer": r[2] if r[2] else "—",
                "Date": r[3].strftime("%Y-%m-%d") if r[3] else "",
                "Time": r[4] if r[4] else "",
                "Category": r[5],
                "User": r[6],
                "Status": r[7]
            }
            for r in results
        ]

    # Generate report by Month
    def get_requests_by_month(self, date):
        """
        Fetch all requests for the month of the given date.
        `date` is expected to be a string in 'YYYY-MM-DD' format.
        """
        query = """
        SELECT 
            r.requestID, 
            r.reqDescription, 
            r.volunteer,
            r.helpNeededDate, 
            TIME_FORMAT(r.helpNeededTime, '%H:%i') AS helpNeededTime,
            c.category AS category_name,
            u.name AS user_name, 
            r.reqStatus
        FROM Request r
        LEFT JOIN Category c ON r.category = c.category
        LEFT JOIN UserAccount u ON r.userID = u.userID
        WHERE YEAR(r.helpNeededDate) = YEAR(%s) AND MONTH(r.helpNeededDate) = MONTH(%s)
        ORDER BY r.helpNeededDate ASC, r.helpNeededTime ASC
        """
        results = self.db.fetch(query, (date, date))

        report = []
        for r in results:
            report.append({
                "Request ID": r[0],
                "Description": r[1],
                "Volunteer": r[2] if r[2] else "—",
                "Date": r[3].strftime("%Y-%m-%d") if r[3] else "",
                "Time": r[4] if r[4] else "",
                "Category": r[5],
                "User": r[6],
                "Status": r[7]
            })

        return report


