from flask import request, Flask, redirect, session, render_template
import private.database
from private.utils import NavBarType

def verify_token():

    if "user" in session:
        return True

    return False

def custom_template(
    site_page : str,
    title : str,
    description : str,
    styles : list,
    navbar_type : int = NavBarType.nonavbar,
    **context
):
    
    theme = request.cookies.get("theme")
    return render_template("index.html", site_page=site_page,title=title,description=description,styles=styles, navbar_type=navbar_type, theme=theme, **context)

def routes(app : Flask):

    @app.route("/")
    def index():
        
        return custom_template("pages/home.html", "SendOver - Home", "", ["/static/css/pages/home.css"], NavBarType.navbar)
    

    # app
    @app.route("/app/login")
    @app.route("/app/login/")
    def login():

        is_connected = verify_token()

        if is_connected:

            if request.args.get("return_url") == None:
                red = redirect("/")
            else:
                red = redirect(request.args.get("return_url"))
            
            return red
        
        return custom_template("pages/app/login.html", "SendOver - Login", "", ["/static/css/pages/app/login.css"], NavBarType.nonavbar)
                

    @app.errorhandler(404)
    def not_found(e):
        return render_template("./errors/404.html")
    
    @app.route("/dark")
    def test():
        red = redirect("/")
        red.set_cookie("theme", "dark", expires=None)
        return red