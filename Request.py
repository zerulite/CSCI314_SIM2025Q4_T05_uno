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
                password="Splatoon2!",  
                database="csit314",
                autocommit=True,         
            )
            print("DB: connected (autocommit ON)")
        except Error as err:
            print(f"DB error: {err}")
            self.connection = None

    def _ensure_conn(self):
        if self.connection is None or not self.connection.is_connected():
            self.connect()

    def execute(self, query, values=None):
        self._ensure_conn()
        cur = self.connection.cursor()
        try:
            cur.execute(query, values or ())
            return cur.rowcount
        finally:
            cur.close()

    def fetch(self, query, values=None):
        self._ensure_conn()
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


