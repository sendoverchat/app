from flask import request, Flask, redirect, session, render_template
import private.database
from private.utils import NavBarType, custom_template, verify_token
from flask_bcrypt import Bcrypt

def routes(app):

    bcrypt = Bcrypt(app)

    # app
    @app.route("/app/login", methods=["POST", "GET"])
    @app.route("/app/login/", methods=["POST", "GET"])
    def login():

        is_connected = verify_token()

        if is_connected:

            if request.args.get("return_url") == None:
                red = redirect("/")
            else:
                red = redirect(request.args.get("return_url"))
            
            return red
        
        return custom_template("pages/app/login.html", "SendOver - Login", "", ["/static/css/pages/app/login.css"], NavBarType.nonavbar)