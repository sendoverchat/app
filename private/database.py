import mysql.connector, json

data = json.load(open("config.json", "r"))

connection_params = {
    'host': data['db_host'],
    'user': data['db_user'],
    'password': data["db_password"],
    'database': data['db_name']
}

class User:

    @staticmethod
    def getAll():
        with mysql.connector.connect(**connection_params) as db:
            with db.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM users")
                return cursor.fetchall()

    @staticmethod
    def getByEmail(email):
        with mysql.connector.connect(**connection_params) as db:
            with db.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM users WHERE user_email = %s", (email,))
                return cursor.fetchall()
            
    @staticmethod
    def getByID(id):
        with mysql.connector.connect(**connection_params) as db:
            with db.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM users WHERE user_id = %s", (id,))
                return cursor.fetchall()
    
    @staticmethod
    def getByUsername(username):
        with mysql.connector.connect(**connection_params) as db:
            with db.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                return cursor.fetchall()