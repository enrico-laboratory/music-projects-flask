import logging

from dotenv import load_dotenv
from flask import Flask

from flask_smorest import Api
from flask_jwt_extended import JWTManager
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

from authenticator.table import Base


load_dotenv('.env-authenticator')

logging.basicConfig(format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

MUSIC_PROJECT_SQLITE_DB_FOLDER = 'instance'
MUSIC_PROJECT_SQLITE_DB_FILENAME = 'authenticator.db'
MUSIC_PROJECTS_SQLITE_DB_URL = 'sqlite:///{folder}/{filename}'


engine = create_engine(MUSIC_PROJECTS_SQLITE_DB_URL.format(
    folder=MUSIC_PROJECT_SQLITE_DB_FOLDER, filename=MUSIC_PROJECT_SQLITE_DB_FILENAME), echo=True)

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object('authenticator.config')

api = Api(app)
jwt = JWTManager(app)

db.init_app(app)

with app.app_context():
    Base.metadata.create_all(engine)

from authenticator.routes import blp
    
api.register_blueprint(blp, url_prefix='/api')



