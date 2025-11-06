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
            self.cursor = self.connection.cursor(dictionary=True)
            print("Database connected successfully!")
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")

    def execute(self, query, values=None):
        try:
            self.cursor.execute(query, values or ())
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Query execution error: {err}")

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
    
    def commit(self):
        self.connection.commit()  # Add this method

class UserProfile:
    def __init__(self):
        self.db = Database()

    # Create Profile
    def create_profile(self, profile, description, profileState):
        # Check if any field is empty
        if not all([profile, description, profileState]):
            return {"message": "Failed to create user: all fields are required."}

        # Check if user already exists
        check_profile_sql = "SELECT * FROM UserProfile WHERE profile = %s"
        if self.db.fetch(check_profile_sql, (profile,)):
            return {"message": f"User {profile} already exists."}

        # Insert new profile
        sql = "INSERT INTO UserProfile (profile, description, profileState) VALUES (%s, %s, %s)"
        values = (profile, description, profileState)
        self.db.execute(sql, values)
        return {"message": f"Profile {profile} successfully created."}
    
    #View Profile
    def view_profile(self, profile):
        sql = "SELECT * FROM UserProfile WHERE profile = %s"
        result = self.db.fetch(sql, (profile,))
        if not result:
            return None
        return result[0]

    # List all Profiles
    def list_profile(self):
        sql = "SELECT * FROM UserProfile"
        return self.db.fetch(sql)
    
    #Update Profile
    def update_profile(self, profile, description, profileState):
        check_sql = "SELECT * FROM UserProfile WHERE profile = %s"
        if self.db.fetch(check_sql, (profile,)):
            sql = """UPDATE UserProfile
                     SET description=%s, profileState=%s
                     WHERE profile=%s"""
            values = (description, profileState, profile)
            self.db.execute(sql, values)
            return {"message": f"Profile {profile} updated successfully."}
        else:
            return {"message": f"Profile {profile} update failed — not found."}

    #Suspend Profile
    def suspend_profile(self, profile, profileState):
        # Normalize case
        profileState = profileState.lower()

        # Check if the profile is active
        check_sql = "SELECT profileState FROM UserProfile WHERE profile = %s"
        result = self.db.fetch(check_sql, (profile,))
        
        if not result:
            return {"message": f"Profile '{profile}' not active."}

        # Current state in the database
        current_state = result[0]['profileState'].lower()

        # If already in the desired state
        if current_state == profileState:
            return {"message": f"User '{profile}' is already in state '{profileState}'."}

        # Update the profileState
        update_sql = "UPDATE UserProfile SET profileState=%s WHERE profile=%s"
        self.db.execute(update_sql, (profileState, profile))
        self.db.commit()  # commit the change

        # Return a message showing the old and new states
        return {
            "message": f"User '{profile}' state updated from '{current_state}' to '{profileState}'."
        }

    #Search User Profile
    def search_profiles(self, **kwargs):
    # Remove empty values
        search_fields = {k: v for k, v in kwargs.items() if v}

    # Return empty list if nothing to search
        if not search_fields:
            return []

        query = "SELECT * FROM UserProfile WHERE 1=1"
        params = []

        for field in ['profile', 'description', 'profileState']:
            value = search_fields.get(field)
            if value:
            # Allow partial matches for both text fields
                query += f" AND {field} LIKE %s"
                params.append(f"%{value}%")

        return self.db.fetch(query, params)

    
