from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv('.env-frontend')

app = Flask(__name__)
app.config.from_object('frontend.config')
jwt = JWTManager(app)

from frontend.routes import project
from frontend.routes.project import project_blp
from frontend.routes.main import blp
from frontend.helpers import is_authenticated

app.register_blueprint(project_blp, url_prefix='/project')
app.register_blueprint(blp, url_prefix='/')

@app.context_processor
def inject_auth_status():
    return {'is_authenticated': is_authenticated()}