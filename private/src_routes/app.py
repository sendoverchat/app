from flask import request, Flask, redirect, session, render_template
import private.database as db
from private.utils import NavBarType, custom_template, verify_token, sendEmail
from flask_bcrypt import Bcrypt

def routes(app):

    bcrypt = Bcrypt(app)

    # app
    @app.route("/app/login", methods=["POST", "GET"])
    @app.route("/app/login/", methods=["POST", "GET"])
    def login():

        error = "none"
        if request.form.get("username") != None and request.form.get("password"):
            
            username = request.form.get("username")
            password = request.form.get("password")

            user_get = db.User.getByUsername(username.lower())

            if user_get == None:
                error = "Incorrect username or password."
            else:
                if bcrypt.check_password_hash(user_get["user_password"], password):
                    
                    session["temp_user"] = user_get

                    red = redirect("/app/a2f")
                    return red
                    
                else:
                    error = "Incorrect username or password."
                


        is_connected = verify_token()

        if is_connected:

            if request.args.get("return_url") == None:
                red = redirect("/")
            else:
                red = redirect(request.args.get("return_url"))
            
            return red
        
        return custom_template("pages/app/login.html", "SendOver - Login", "", ["/static/css/pages/app/login.css"], NavBarType.nonavbar, error=error)
    
    @app.route("/app/register", methods=["POST", "GET"])
    @app.route("/app/register/", methods=["POST", "GET"])
    def register():
        
        is_connected = verify_token()

        if is_connected:
            if request.args.get("return_url") == None:
                red = redirect("/")
            else:
                red = redirect(request.args.get("return_url"))
            
            return red
        
        return custom_template("pages/app/register.html", "SendOver - Register", "", ["/static/css/pages/app/register.css"], NavBarType.nonavbar)
    
    @app.route("/app/a2f", methods=["POST", "GET"])
    @app.route("/app/a2f/", methods=["POST", "GET"])
    def a2f():

        if request.form.get("emailcode") != None:

            code = request.form.get("emailcode")

            user = session.get("temp_user")
            email = user["user_email"]

            dbauth = db.Auth_Code.getlast(email)

            if dbauth == None:

                error = "This code is invalide !"

                return custom_template("pages/app/a2f.html", "SendOver - a2f", "", ["/static/css/pages/app/login.css"], NavBarType.nonavbar, error=error)
            
            elif dbauth["auth_uses"] >= 1 or str(dbauth["auth_code"]) != str(code):
                error = "This code is invalide !"

                return custom_template("pages/app/a2f.html", "SendOver - a2f", "", ["/static/css/pages/app/login.css"], NavBarType.nonavbar, error=error)
            else:
                db.Auth_Code.updateUses(dbauth["auth_code_id"])
                session["user"] = session["temp_user"]
                red = redirect("/")

                return red


        
        is_connected = verify_token()

        if is_connected:
            if request.args.get("return_url") == None:
                red = redirect("/")
            else:
                red = redirect(request.args.get("return_url"))
            
            return red
        
        if session.get("temp_user") == None:
            red = redirect("/")
            return red
        
        user = session.get("temp_user")
        email = user["user_email"]

        sendEmail("Auth Code", "Your auth code is : <strong>"+str(db.Auth_Code.insert(email))+"</strong>", email)

        return custom_template("pages/app/a2f.html", "SendOver - a2f", "", ["/static/css/pages/app/login.css"], NavBarType.nonavbar, error="none")