from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

backend_dir = os.path.dirname(os.path.abspath(__file__))
instance_folder_path = os.path.join(backend_dir, "../database/instance")

app = Flask(
    __name__,
    instance_path=instance_folder_path,
    template_folder="../frontend/templates",
    static_folder="../frontend/static",
)

app.secret_key = "whatinthehellamisupposedtowritehere?generateanultrastrongpassword?"

login_manager = LoginManager()
login_manager.init_app(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    app.instance_path, "db_51.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
