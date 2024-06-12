from flask import Flask
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

from private.routes import routes
routes(app)

app.secret_key = 'c64f3b67-b6e2-4185-a58c-3540969e0c81'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = "./static"

app.run("0.0.0.0", 8090)