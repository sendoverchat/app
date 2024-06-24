from flask import Flask
import json

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

try:
    # import routes
    from private.routes import routes
    routes(app)
except Exception as e:
    print("Exeception : "+str(e))

# config
app.secret_key = json.load(open("config.json", "r"))["secret-key"]
app.config['SESSION_TYPE'] = 'filesystem'
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = "./static"

app.run("0.0.0.0", 8090, debug=True)