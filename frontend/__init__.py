from flask import Flask
from dotenv import load_dotenv

from frontend import config 

load_dotenv()

app = Flask(__name__)
app.config.from_envvar('CONFIG_FILE_PATH')


from frontend import routes
from frontend.routes import project_blp


app.register_blueprint(project_blp, url_prefix='/project')
