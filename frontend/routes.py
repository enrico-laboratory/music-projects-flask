import json
from datetime import datetime
from dateutil.parser import parse
from pprint import pprint as pp

from flask import Blueprint, render_template, request
import requests

from frontend import app, config
from frontend.schemas import TaskSchema

project_blp = Blueprint('project', __name__)

@app.route('/')
def home():
    return render_template('home.html.jinja')


@project_blp.route('/')
def project():
    url = f'{config.BACKEND_HOSTNAME}:{config.BACKEND_PORT}/music_project'
    projects = json.loads(requests.get(url=url).text)   
    return render_template('project.html.jinja', projects=projects)

@project_blp.route('/tasks/<project_name>')
def tasks(project_name):
    url = f'{config.BACKEND_HOSTNAME}:{config.BACKEND_PORT}/api/task'
    sort = request.args.get('sort', 'newer')
    params = {'filter': project_name,
              'sort': sort}
    tasks = json.loads(requests.get(url=url, params=params).text)
    
    pp(tasks)

    return render_template('task.html.jinja', tasks=tasks)

@project_blp.app_template_filter()
def format_datetime(date_str: str, format='datetime'):
    date = "%a %d %b %y"
    time = "%-H:%M"
    strftime = ""
    match format:
        case 'datetime':
            strftime = f'{date} {time}'
        case 'date':
            strftime = date
        case 'time':
            strftime = time
    
    return parse(date_str).strftime(strftime)