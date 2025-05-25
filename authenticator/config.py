from os import getenv

PROPAGATE_EXCEPTIONS = True
API_TITLE = "Authenticator REST API"
API_VERSION = "v1"
OPENAPI_VERSION = "3.0.3"
OPENAPI_URL_PREFIX = "/"
OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
SQLALCHEMY_DATABASE_URI = "sqlite:///auth.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')

MUSIC_PROJECT_SQLITE_DB_FOLDER = 'instance'
MUSIC_PROJECT_SQLITE_DB_FILENAME = 'authenticator.db'
MUSIC_PROJECTS_SQLITE_DB_URL = 'sqlite:///{folder}/{filename}'