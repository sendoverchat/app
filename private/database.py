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
                return cursor.fetchone()
            
    @staticmethod
    def updateUses(id):
        uses = 0
        with mysql.connector.connect(**connection_params) as db:
            with db.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM auth_codes WHERE auth_code_id = %s", (id,))
                uses = cursor.fetchone()["auth_uses"]
        uses += 1
        print(uses)
        with mysql.connector.connect(**connection_params) as db:
            with db.cursor() as cursor:
                cursor.execute("UPDATE auth_codes SET auth_uses = %s WHERE auth_code_id = %s", (uses, id,))
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