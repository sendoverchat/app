from flask import request, Flask, redirect, session, render_template, abort, jsonify
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
        
        
        form = request.json

        if form.get("user_id") != None:

            user = db.User.getByToken(session.get("token"))
            user_id = user["user_id"]
            receveur_id = form.get("user_id")

            db.FriendRequests.insert(user_id, receveur_id)

            return jsonify({"success" : "Friend request send !"})
            
        else:
            red = redirect("/")
            return red

