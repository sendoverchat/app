import mysql.connector, json, random, time

data = json.load(open("config.json", "r"))

connection_params = {
    'host': data['db_host'],
    'user': data['db_user'],
    'password': data["db_password"],
    'database': data['db_name']
}

class Auth_Code:

    @staticmethod
    def getlast(email):
        timestamp = round(time.time()) - (60*5)
        with mysql.connector.connect(**connection_params) as db:
            with db.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM auth_codes WHERE auth_email = %s AND auth_exp > %s AND auth_uses = 0", (email, timestamp))
                codes = cursor.fetchall()
                return codes[-1]
            
    @staticmethod
    def updateUses(id):
        uses = 0
        with mysql.connector.connect(**connection_params) as db:
            with db.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM auth_codes WHERE auth_code_id = %s", (id,))
                code = cursor.fetchone()
    

        with mysql.connector.connect(**connection_params) as db:
            with db.cursor() as cursor:
                cursor.execute("DELETE FROM auth_codes WHERE auth_email = %s", (code["auth_email"],))
                db.commit()
            

    @staticmethod
    def insert(email):
        # if 
            code = ""
            for i in range(0, 6):
                code += str(random.randint(0, 9))
            exp = round(time.time()) + (60 * 5)
            with mysql.connector.connect(**connection_params) as db:
                with db.cursor() as cursor:
                    cursor.execute("INSERT INTO auth_codes (auth_code, auth_email, auth_exp) VALUES (%s, %s, %s)", (code, email, exp,))
                    db.commit()

            return code
    
class User:

    @staticmethod
    def insertUser(username, user_email, user_password, avatar):
        with mysql.connector.connect(**connection_params) as db:
            with db.cursor() as cursor:
                cursor.execute("INSERT INTO users (username, displayname, user_email, user_password, avatar) VALUES (%s, %s, %s, %s, %s)", (username, username, user_email, user_password, avatar,))
                db.commit()

    @staticmethod
    def countUsername(username):
        with mysql.connector.connect(**connection_params) as db:
            with db.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username,))
                return cursor.fetchone()[0]
            
    @staticmethod
    def countEmail(email):
        with mysql.connector.connect(**connection_params) as db:
            with db.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM users WHERE user_email = %s", (email,))
                return cursor.fetchone()[0]

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
                return cursor.fetchone()
            
    @staticmethod
    def getByID(id):
        with mysql.connector.connect(**connection_params) as db:
            with db.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM users WHERE user_id = %s", (id,))
                return cursor.fetchone()
    
    @staticmethod
    def getByUsername(username):
        with mysql.connector.connect(**connection_params) as db:
            with db.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                return cursor.fetchone()