from flask import request, Flask, redirect, session, render_template
import private.database

class NavBarType:
    nonavbar = 0
    navbar = 1
    sidebar = 2



def custom_template(
    site_page : str,
    title : str,
    description : str,
    styles : list,
    navbar_type : int = NavBarType.nonavbar,
    **context
):
    
    cookie_theme = request.cookies.get("theme")
    if cookie_theme == "black":
        theme_black = True
    else:
        theme_black = False
    return render_template("index.html", site_page=site_page,title=title,description=description,styles=styles, navbar_type=navbar_type, theme_black=theme_black, **context)



def routes(app : Flask):

    @app.route("/")
    def index():
        
        return custom_template("pages/home.html", "SendOver - Home", "", ["/static/css/home.css"], NavBarType.navbar)

    
    @app.errorhandler(404)
    def not_found(e):
        return render_template("./errors/404.html")