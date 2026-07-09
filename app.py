from flask import Flask
from config import *
from flask_wtf import CSRFProtect
from extentions import db
from blueprints.general import bp as general

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = MYSQL_CONFIG
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = SECRET_KEY

csrf = CSRFProtect(app)
db.init_app(app)

app.register_blueprint(general)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
