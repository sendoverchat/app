import mysql.connector, json, random, time
from uuid import uuid4
data = json.load(open("config.json", "r"))

connection_params = {
    'host': data['db_host'],
    'user': data['db_user'],
    'password': data["db_password"],
    'database': data['db_name']
}

class Friends:
    @staticmethod
    def getAllByUserId(user_id):
        with mysql.connector.connect(**connection_params) as db:
            with db.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM friends WHERE friend_1 = %s OR friend_2 = %s", (user_id, user_id,))

                return cursor.fetchall()

    @staticmethod
    def get(user_1, user_2):
        with mysql.connector.connect(**connection_params) as db:
            with db.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM friends WHERE (friend_1 = %s AND friend_2 = %s) OR (friend_1 = %s AND friend_2 = %s)", (user_1, user_2, user_2, user_1,))

                return cursor.fetchall()

    @staticmethod
    def insert(user_1, user_2):

        if(len(Friends.get(user_1, user_2)) == 0):

            with mysql.connector.connect(**connection_params) as db:
                with db.cursor() as cursor:
                    cursor.execute("INSERT INTO friends (friend_1, friend_2) VALUES (%s, %s)", (user_1, user_2,))     
                    db.commit()
    
    @staticmethod
    def drop(user_1, user_2):
        if(len(Friends.get(user_1, user_2)) == 1):
            with mysql.connector.connect(**connection_params) as db:
                with db.cursor() as cursor:
                    cursor.execute("DELETE FROM friends WHERE (friend_1 = %s AND friend_2 = %s) OR (friend_1 = %s AND friend_2 = %s)", (user_1, user_2, user_2, user_1,))
                    db.commit()

class FriendRequests:
    @staticmethod
    def getAllByReceveurId(receveur_id):
        with mysql.connector.connect(**connection_params) as db:
            with db.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM friend_requests WHERE friend_receveur = %s", (receveur_id,))
                return cursor.fetchall()

    @staticmethod
    def get(sender_id, receveur_id):
        with mysql.connector.connect(**connection_params) as db:
            with db.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM friend_requests WHERE friend_sender = %s AND friend_receveur = %s", (sender_id, receveur_id,))
                return cursor.fetchall()
            
    @staticmethod
    def drop(sender_id, receveur_id):
        if len(FriendRequests.get(sender_id, receveur_id)) == 1:
            with mysql.connector.connect(**connection_params) as db:
                with db.cursor() as cursor:
                    cursor.execute("DELETE FROM friend_requests WHERE friend_sender = %s AND friend_receveur = %s", (sender_id, receveur_id,))
                    db.commit()

    
    @staticmethod
    def insert(sender_id, receveur_id):
        if len(FriendRequests.get(receveur_id, sender_id) == 1):
            Friends.insert(receveur_id, sender_id)
            FriendRequests.drop(receveur_id, sender_id)
        else:
            with mysql.connector.connect(**connection_params) as db:
                with db.cursor() as cursor:
                    cursor.execute("INSERT INTO friend_requests (friend_sender, friend_receveur) VALUES (%s, %s)", (sender_id, receveur_id,))
                    db.commit()

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
                cursor.execute("INSERT INTO users (username, displayname, user_email, user_password, avatar, token) VALUES (%s, %s, %s, %s, %s, %s)", (username, username, user_email, user_password, avatar, uuid4(),))
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
    def getByToken(token):
        if token == None:
            return None
        with mysql.connector.connect(**connection_params) as db:
            with db.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM users WHERE token = %s", (token,))
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