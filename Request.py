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
            "SELECT r.requestID, r.request, r.date, r.time, r.category, r.userID, r.completed "
            "FROM `Request` r "
            "LEFT JOIN `UserAccount` u ON u.userID = r.userID "
            "WHERE 1=1"
        )
        params = []

        for field in ["requestID", "request", "date", "time", "category", "userID", "completed"]:
            value = kwargs.get(field)
            if value is not None and value != "":
                if field == "request":
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

    #View All Requests
    def view_all_requests(self, limit=100, offset=0):
        sql = (
            "SELECT r.requestID, r.request, r.date, r.time, r.category, r.userID, r.completed "
            "FROM `Request` r "
            "ORDER BY r.date, r.time, r.requestID "
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
        csr_user_id: str,
        requestID=None,
        request=None,
        date=None,
        time=None,
        category=None,
        userID=None,
        completed=None,
        limit: int = 50,
        offset: int = 0,
    ):
        sql = [
            "SELECT r.requestID, r.request, r.date, r.time, r.category, r.userID, r.completed",
            "FROM Request r",
            "INNER JOIN RequestShortlist s ON s.requestID = r.requestID",
            "WHERE s.userID = %s",
        ]
        params = [csr_user_id]

        if requestID:
            sql.append("AND r.requestID = %s")
            params.append(requestID)

        if request is not None and request != "":
            sql.append("AND r.request LIKE %s")
            params.append(f"%{request}%")

        if date:
            sql.append("AND r.date = %s")
            params.append(date)

        if time:
            sql.append("AND r.time = %s")
            params.append(time)

        if category:
            sql.append("AND r.category LIKE %s")
            params.append(f"%{category}%")

        if userID:
            sql.append("AND r.userID LIKE %s")
            params.append(f"%{userID}%")

        if completed is not None:
            sql.append("AND (r.completed = %s OR (r.completed IS NULL AND %s = ''))")
            params.extend([completed, completed])

        sql.append("ORDER BY r.requestID LIMIT %s OFFSET %s")
        params.extend([int(limit), int(offset)])

        return self.db.fetch(" ".join(sql), tuple(params))
    
    #View Shortlisted Requests
    def view_shortlist(self, csr_user_id: str, limit=100, offset=0):
        sql = (
            "SELECT r.requestID, r.request, r.date, r.time, r.category, r.userID, r.completed "
            "FROM `Request` r "
            "INNER JOIN `RequestShortlist` s ON s.requestID = r.requestID "
            "WHERE s.userID = %s "
            "ORDER BY r.date, r.time, r.requestID "
            "LIMIT %s OFFSET %s"
        )
        return self.db.fetch(sql, (csr_user_id, int(limit), int(offset)))
