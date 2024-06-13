from flask import request, Flask, redirect, session, render_template
import private.database

def custom_template(
    site_page : str,
    title : str,
    description : str,
    styles : list,
    **context
):
    return render_template("index.html", site_page=site_page,title=title,description=description,styles=styles, **context)



def routes(app : Flask):

    @app.route("/")
    def index():
        
        return custom_template("home.html", "SendOver - Home", description="", styles=["/static/css/home.css"])

    
    @app.errorhandler(404)
    def not_found(e):
        return render_template("./errors/404.html")