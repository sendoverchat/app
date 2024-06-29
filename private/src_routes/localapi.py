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
        
    @app.route("/api/local/deniedFriend", methods=["POST"])
    def deniedFriend():

        is_token = session.get("token") != None

        if not is_token:
            red = redirect("/")
            return red
        
        
        form = request.json

        if form.get("user_id") != None:

            user = db.User.getByToken(session.get("token"))
            receveur_id = user["user_id"]
            sender_id = form.get("user_id")

            db.FriendRequests.drop(sender_id, receveur_id)
            db.FriendRequests.drop(receveur_id, sender_id)

            return jsonify({"success" : "Friend request denied with success !"})
            
        else:
            red = redirect("/")
            return red

    @app.route("/api/local/deleteFriend", methods=["POST"])
    def delFriend():

        is_token = session.get("token") != None

        if not is_token:
            red = redirect("/")
            return red
        
        
        form = request.json

        if form.get("user_id") != None:

            user = db.User.getByToken(session.get("token"))
            receveur_id = user["user_id"]
            sender_id = form.get("user_id")

            db.Friends.drop(sender_id, receveur_id)

            return jsonify({"success" : "Friend delete with success !"})
            
        else:
            red = redirect("/")
            return red



