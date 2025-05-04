import logging

from dotenv import load_dotenv
from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from backend.db import db
from backend.projects import blp as project_blp

load_dotenv('.env-backend')

logging.basicConfig(format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def create_app() -> Flask:

    app = Flask(__name__)
    app.config.from_object('backend.config')
    
    api = Api(app)
    
    jwt = JWTManager(app)
    
    api.register_blueprint(project_blp, url_prefix='/projects')

    db.init_app(app)

    return app
