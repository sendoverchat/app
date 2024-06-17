from flask import request, Flask, redirect, session, render_template
import private.database as db
from private.utils import NavBarType, custom_template, sendEmail
from flask_bcrypt import Bcrypt
import random

def routes(app : Flask):

    bcrypt = Bcrypt(app)


    @app.route("/app/guild")
    @app.route("/app/guild/")
    def guild():

        is_token = session.get("token") != None

        if not is_token:
            red = redirect("/app/login?return_url=/app/guild")
            return red
        
        user = db.User.getByToken(session["token"])

        return custom_template(site_page="pages/app/guild.html", title="SendOver - Guild", description="", styles=["/static/css/pages/app/guild.css"], navbar_type=NavBarType.sidebar, user=user)

    @app.route("/app/friend")
    @app.route("/app/friend/")
    def friend():

        is_token = session.get("token") != None
        
        if not is_token:
            red = redirect("/app/login?return_url=/app/friend")
            return red
        
        print(session["token"]) 
        user = db.User.getByToken(session["token"])

        return custom_template(site_page="pages/app/friend.html", title="SendOver - Friend", description="", styles=["/static/css/pages/app/friend.css"], navbar_type=NavBarType.sidebar, user=user)


    # login register a2f
    @app.route("/app/login", methods=["POST", "GET"])
    @app.route("/app/login/", methods=["POST", "GET"])
    def login():

        is_token = session.get("token") != None

        if is_token:

            if request.args.get("return_url") == None:
                red = redirect("/")
            else:
                red = redirect(request.args.get("return_url"))
            
            return red

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
                    url = session["return_url"]
                    
                    if url == None:
                        red = redirect("/app/a2f")
                    else:
                        red = redirect("/app/a2f?return_url="+url)
                    return red
                    
                else:
                    error = "Incorrect username or password."
        
        session['return_url'] = request.args.get("return_url")

        return custom_template("pages/app/login.html", "SendOver - Login", "", ["/static/css/pages/app/login.css"], NavBarType.nonavbar, error=error)
    
    @app.route("/app/register", methods=["POST", "GET"])
    @app.route("/app/register/", methods=["POST", "GET"])
    def register():
        
        is_token = session.get("token") != None
        
        if is_token:
            if request.args.get("return_url") == None:
                red = redirect("/")
            else:
                red = redirect(request.args.get("return_url"))
            
            return red
        
        form = request.form
        
        if form.get("username") != None and form.get("password") != None and form.get("password_comfirm") and form.get("email"):

            username = form.get("username")
            password = form.get("password")
            password_comfirm = form.get("password_comfirm")
            email = form.get("email")

            countUser = db.User.countUsername(username)
            countEmail = db.User.countEmail(email)

            if len(username) < 3 or len(username) > 20:
                return custom_template("pages/app/register.html", "SendOver - Register", "", ["/static/css/pages/app/register.css"], NavBarType.nonavbar, error="The username must be between 3 and 20 characters long.") 
            elif countUser == 1:
                return custom_template("pages/app/register.html", "SendOver - Register", "", ["/static/css/pages/app/register.css"], NavBarType.nonavbar, error="This username is already taken.")

            if len(password) < 6:
                return custom_template("pages/app/register.html", "SendOver - Register", "", ["/static/css/pages/app/register.css"], NavBarType.nonavbar, error="Password size must be at least 6 characters long.")

            if password != password_comfirm:
                return custom_template("pages/app/register.html", "SendOver - Register", "", ["/static/css/pages/app/register.css"], NavBarType.nonavbar, error="The password doesn't match.")
            
            if countEmail == 1:
                return custom_template("pages/app/register.html", "SendOver - Register", "", ["/static/css/pages/app/register.css"], NavBarType.nonavbar, error="This email is already taken.")
            
            session["temp_user"] = {
                "username" : username,
                "user_email" : email,
                "displayname" : username,
                "user_password" : bcrypt.generate_password_hash(password),
                "user_status" : 0,
                "nocreate" : True
            }

            url = session["return_url"]
            if url == None:
                red = redirect("/app/a2f")
            else:
                red = redirect("/app/a2f?return_url="+url)
            return red
        
        session['return_url'] = request.args.get("return_url")

        return custom_template("pages/app/register.html", "SendOver - Register", "", ["/static/css/pages/app/register.css"], NavBarType.nonavbar, error="none")
    
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

                # create account :
                if "nocreate" in user:
                    
                    db.User.insertUser(user["username"].lower(), user["user_email"], user["user_password"], f"/static/assets/default_avatars/avatar{random.randint(1, 4)}.png")

                db.Auth_Code.updateUses(dbauth["auth_code_id"])
                session["token"] = db.User.getByEmail(session["temp_user"]["user_email"])["token"]
                url = session["return_url"]
                if url != None:
                    red = redirect(url)
                else:
                    red = redirect("/")
                return red


        
        is_token = session.get("token") != None
        
        if is_token:
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

        session['return_url'] = request.args.get("return_url")

        return custom_template("pages/app/a2f.html", "SendOver - a2f", "", ["/static/css/pages/app/login.css"], NavBarType.nonavbar, error="none")