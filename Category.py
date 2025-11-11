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
                password="0000", #Change this if needed
                database="csitc"
            )
            self.cursor = self.connection.cursor(dictionary=True)
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

class Category:
    def __init__(self):
        self.db = Database()

    #Create Category
    def createCategory(self, category, description):
        #Check if any field is empty
        if not all([category, description]):
            return {"message": "Failed to create category: all fields are required."}

        #Check if category already exists
        check_user_sql = "SELECT * FROM Category WHERE category = %s"
        if self.db.fetch(check_user_sql, (category,)):
            return {"message": f"Category {category} already exists."}

        #Insert new category
        sql = """INSERT INTO Category
                (category, description)
                VALUES (%s, %s)"""
        values = (category, description)
        self.db.execute(sql, values)
        return {"message": f"Category {category} successfully created."}


    # View Account
    def viewCategory(self, category):
        sql = "SELECT * FROM Category WHERE category = %s"
        result = self.db.fetch(sql, (category,))
        if not result:
            return None
        return result[0]

    # List all Accounts
    def listCategory(self):
        sql = "SELECT category, description FROM Category"
        return self.db.fetch(sql)

    #Update Category
    def updateCategory(self, category, description):
        check_sql = "SELECT * FROM Category WHERE category = %s"
        if self.db.fetch(check_sql, (category,)):
            sql = """UPDATE Category
                     SET description=%s
                     WHERE category=%s"""
            values = (description, category)
            self.db.execute(sql, values)
            return {"message": f"Category {category} updated successfully."}
        else:
            return {"message": f"Category {category} update failed — not found."}

    #Delete Category
    def deleteCategory(self, category):
            if not category:
                return {"success": False, "message": "Category is required."}

            check_sql = "SELECT category, description FROM Category WHERE category = %s"
            result = self.db.fetch(check_sql, (category,))

            if not result:
                return {"success": False, "message": f"Category '{category}' does not exist."}

            description = result[0]["description"]

            delete_sql = "DELETE FROM Category WHERE category = %s"
            try:
                self.db.cursor.execute(delete_sql, (category,))
                self.db.connection.commit()
                return {
                    "success": True,
                    "message": f"Category '{category}' with description '{description}' deleted successfully."
                }
            except Exception as e:
                return {"success": False, "message": str(e)}
            
    #Search Category
    def searchCategory(self, **kwargs):
        # Remove empty values
        search_fields = {k: v for k, v in kwargs.items() if v}

        # Return empty list if nothing to search
        if not search_fields:
            return []

        query = "SELECT * FROM Category WHERE 1=1"
        params = []

        # Loop over individual fields
        for field in ['category', 'description']:
            value = search_fields.get(field)
            if value:
                query += f" AND {field} LIKE %s"
                params.append(f"%{value}%")

        return self.db.fetch(query, params)
