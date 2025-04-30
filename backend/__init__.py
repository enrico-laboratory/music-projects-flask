import logging
from os import getenv

from dotenv import load_dotenv
from flask import Flask
from flask_smorest import Api

from backend.db import db
from backend.projects import blp as project_blp

MUSIC_PROJECT_SQLITE_DB_FOLDER = 'instance/'
MUSIC_PROJECT_SQLITE_DB_FILENAME = 'music_projects.db'
MUSIC_PROJECTS_SQLITE_DB_URL = 'sqlite:///{folder}{filename}'

load_dotenv('.env')

logging.basicConfig(format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def create_app(db_url=None) -> Flask:

    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or getenv(
        "DATABASE_URL", "sqlite:///music_projects.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    api = Api(app)
    api.register_blueprint(project_blp, url_prefix='/projects')

    db.init_app(app)

    return app
