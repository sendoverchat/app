from flask import request, Flask, redirect, session, render_template

def routes(app : Flask):

    @app.route("/")
    def index():

        return render_template('index.html', test="Hello World")
    
    @app.errorhandler(404)
    def not_found(e): 
        return render_template("./errors/404.html") 