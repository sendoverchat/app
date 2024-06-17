from flask import request, Flask, redirect, session, render_template, abort
import private.database as db
from private.utils import NavBarType, custom_template, sendEmail
from flask_bcrypt import Bcrypt

def routes(app : Flask):

    bcrypt = Bcrypt(app)

    @app.route("/api/local/addfriend", methods=["POST"])
    def addfriend():
        
        is_token = session.get("token") != None

        if not is_token:
            red = redirect("/")
            return red
        
        form = request.form

        if form.get("user_id") != None:

            pass
            
        else:
            red = redirect("/")
            return red

