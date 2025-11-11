import mysql.connector

class Database:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "0000"
        self.database = "csitc"
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor(dictionary=True) 
            print(f"Connected to database '{self.database}' successfully!")
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")

    def execute(self, query, values=None):
        try:
            self.cursor.execute(query, values or ())
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Query execution error: {err}")

    def fetch(self, query, values=None):
        self.cursor.execute(query, values or ())
        return self.cursor.fetchall() 

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")


class UserAccount:
    def __init__(self):
        self.db = Database()

    # Create Account
    def createUserAccount(self, userID, password, name, email, profile, userState):
        # Check if any field is empty
        if not all([userID, password, name, email, profile, userState]):
            return {"message": "Failed to create user: all fields are required."}

        # Check if user already exists
        check_user_sql = "SELECT * FROM UserAccount WHERE userID = %s"
        if self.db.fetch(check_user_sql, (userID,)):
            return {"message": f"User {userID} already exists."}
        
        # Check if email already exists
        check_email_sql = "SELECT * FROM UserAccount WHERE email = %s"
        if self.db.fetch(check_email_sql, (email,)):
            return {"message": f"{email} already exists."}
                
        # Insert new user
        sql = """INSERT INTO UserAccount
                (userID, password, name, email, profile, userState)
                VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (userID, password, name, email, profile, userState)
        self.db.execute(sql, values)
        return {"message": f"User {userID} successfully created."}

    # View Account
    def viewUserAccount(self, userID):
        sql = "SELECT * FROM UserAccount WHERE userID = %s"
        result = self.db.fetch(sql, (userID,))
        if not result:
            return None
        return result[0]

    # List all Accounts
    def listUserAccount(self):
        sql = "SELECT userID, name, email, profile, userState FROM UserAccount"
        return self.db.fetch(sql)

    # Update Account
    def updateUserAccount(self, userID, password, name, email, profile, userState):
        check_sql = "SELECT * FROM UserAccount WHERE userID = %s"
        if self.db.fetch(check_sql, (userID,)):
            sql = """UPDATE UserAccount
                     SET password=%s, name=%s, email=%s, profile=%s, userState=%s
                     WHERE userID=%s"""
            values = (password, name, email, profile, userState, userID)
            self.db.execute(sql, values)
            return {"message": f"User {userID} updated successfully."}
        else:
            return {"message": f"User {userID} update failed — not found."}
        
    #Suspend Account
    def suspendUserAccount(self, userID, userState):
        # Normalize case
        userState = userState.lower()

        # Check if the user exists
        check_sql = "SELECT userState FROM UserAccount WHERE userID = %s"
        result = self.db.fetch(check_sql, (userID,))
        
        if not result:
            return {"message": f"User {userID} not found."}

        current_state = result[0]['userState'].lower()

        # If already in the desired state, no change needed
        if current_state == userState:
            if userState == "inactive":
                return {"message": f"User {userID} is already inactive."}
            elif userState == "active":
                return {"message": f"User {userID} is already active."}
            else:
                return {"message": f"User {userID} already in state '{userState}'."}

        # Otherwise, update to the new state
        update_sql = """UPDATE UserAccount
                        SET userState = %s
                        WHERE userID = %s"""
        self.db.execute(update_sql, (userState, userID))

        # Return message depending on what the new state is
        if userState == "inactive":
            return {"message": f"User {userID} suspended successfully."}
        elif userState == "active":
            return {"message": f"User {userID} unsuspended successfully."}
        else:
            return {"message": f"User {userID} updated to state '{userState}' successfully."}


    #Search Account
    def searchUsers(self, **kwargs):
        # Remove empty values
        search_fields = {k: v for k, v in kwargs.items() if v}

        # Return empty list if nothing to search
        if not search_fields:
            return []

        query = "SELECT * FROM UserAccount WHERE 1=1"
        params = []

        for field in ['userID', 'password', 'name', 'email', 'profile', 'userState']:
            value = search_fields.get(field)
            if value:
                if field in ['name', 'email', 'userID']:
                    query += f" AND {field} LIKE %s"
                    params.append(f"%{value}%")
                else:
                    query += f" AND {field} = %s"
                    params.append(value)

        return self.db.fetch(query, params)
    
    #Login
    def loginUser(self, userID, password):
        # Check for missing fields
        if not userID or not password:
            return {"success": False, "message": "All fields are required."}

        # Verify login credentials
        sql = "SELECT userID, name, profile, userState FROM UserAccount WHERE userID=%s AND password=%s"
        result = self.db.fetch(sql, (userID, password))

        if not result:
            return {"success": False, "message": "Invalid userID or password."}

        user = result[0]

        # Check suspension
        if user["userState"].lower() == "inactive":
            return {"success": False, "message": "Your account is suspended."}

        # No redirect logic here anymore
        return {
            "success": True,
            "message": "Login successful.",
            "user": user
        }
    
    def check_profile(self, profile):
        # Fetch the profile state
        check_profile_sql = "SELECT profileState FROM UserProfile WHERE profile = %s"
        result = self.db.fetch(check_profile_sql, (profile,))
        
        if not result:
            return {"success": False, "message": f"Profile '{profile}' does not exist."}
        
        state = result[0]['profileState'].lower()
        if state != 'active':
            return {"success": False, "message": f"Profile '{profile}' is not active (current state: {state})."}
        
        # Profile exists and is active
        return {"success": True, "message": f"Profile '{profile}' is active."}


