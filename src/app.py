from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_session import Session

from config import Config
from db.models import db
import utils as utils

from auth import init_auth
from routes import init_routes
from api import init_api

app = Flask(
    __name__, template_folder="../alpine-app/templates", static_folder="../alpine-app"
)

CORS(app)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
app.config["SESSION_SQLALCHEMY"] = db
Session(app)

with app.app_context():
    db.create_all()

init_auth(app)
init_routes(app)
init_api(app)

if __name__ == "__main__":
    app.run(debug=True)
