import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Keith684485",  
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