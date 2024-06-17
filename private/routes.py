from flask import request, Flask, redirect, session, render_template
import private.database
from private.utils import NavBarType, custom_template
from flask_bcrypt import Bcrypt
import private.src_routes.app as approutes 
import private.src_routes.api as apiroutes
import private.src_routes.localapi as localapiroutes

def routes(app : Flask):

    @app.route("/")
    def index():
        return custom_template("pages/home.html", "SendOver - Home", "", ["/static/css/pages/home.css"], NavBarType.navbar)                

    @app.errorhandler(404)
    def not_found(e):
        return render_template("./errors/404.html")
    
    @app.route("/dark")
    def test():
        red = redirect("/")
        red.set_cookie("theme", "dark", expires=None)
        return red
    
    approutes.routes(app)
    apiroutes.routes(app)
    localapiroutes.routes(app)