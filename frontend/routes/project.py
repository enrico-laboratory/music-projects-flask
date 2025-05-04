import json

from datetime import timedelta
from dateutil.parser import parse


from flask import Blueprint, render_template, request, abort
from flask_jwt_extended import jwt_required
import requests

from frontend import app, config


project_blp = Blueprint('project', __name__)


@project_blp.before_request
@jwt_required()
def before_request():
    """ Protect all of the project endpoints. """
    pass 

@project_blp.route('/')
def projects():
    url = f'{config.BACKEND_PROJECTS_FULL_PATH}/music_project'

    response = requests.get(url=url)
    if not response.status_code == 200:
        abort(500)
    projects = json.loads(response.text)
    
    title = 'Projects'
    return render_template('projects.html.jinja',
                           projects=projects,
                           title=title)


@project_blp.route('/description/<int:project_id>')
def description(project_id):
    url = f'{config.BACKEND_PROJECTS_FULL_PATH}/music_project/{project_id}'

    response = requests.get(url=url)
    if not response.status_code == 200:
        abort(500)
    project = json.loads(response.text)
    title = 'Description'
    return render_template('project/description.html.jinja',
                           project=project,
                           project_id=project_id,
                           title=title)


@project_blp.route('/tasks/<int:project_id>')
def tasks(project_id):
    url = f'{config.BACKEND_PROJECTS_FULL_PATH}/task'
    sort = request.args.get('sort', 'newer')
    params = {'filter': project_id,
              'sort': sort}
    response = requests.get(url=url, params=params)
    if not response.status_code == 200:
        abort(500)
    tasks = json.loads(response.text)
    title = 'Tasks'
    return render_template('project/task.html.jinja',
                           tasks=tasks,
                           project_id=project_id,
                           title=title)


@project_blp.route('/repertoire/<int:project_id>')
def repertoire(project_id):

    repertoire: list[dict] = send_request_with_project_id(
        'part_allocation',
        project_id=project_id,
        sort=False
    )
    
    repertoire.sort(key=lambda music: music['name'])
    title = 'Repertoire'
    return render_template('project/repertoire.html.jinja',
                           repertoire=repertoire,
                           project_id=project_id, 
                           title=title)

@project_blp.route('/part_allocation/<int:project_id>')
def part_allocation(project_id):
    part_allocation: list[dict] = send_request_with_project_id(
        'part_allocation',
        project_id=project_id,
        sort=False
    )
    part_allocation.sort(key=lambda music: music['name'])
    part_allocation_range = get_divisi_range(part_allocation)
    title='Part Allocation'
    return render_template('project/divisi.html.jinja',
                           part_allocation=part_allocation,
                           project_id=project_id,
                           part_allocation_range=part_allocation_range,
                           title=title)

@project_blp.route('/cast/<int:project_id>')
def cast(project_id):
    cast: list[dict] = send_request_with_project_id(
        'role',
        project_id=project_id,
        sort=False
    )
    
    sort_order = {'S':0,'S1':1,'S2':2,'S3':4,
                  'A':5,'A1':6,'A2':7,'A3':8,
                  'T':9,'T1':10,'T2':11,'T3':12,
                  'B':13,'B1':14,'B2':15,'B3':16,}
    cast.sort(key=lambda x: sort_order[x['name']])
    title = 'Cast'
    return render_template('project/cast.html.jinja',
                           cast=cast,
                           project_id=project_id,
                           title=title)


# Filters
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

@project_blp.app_template_filter()
def format_duration(duration: str):
    td = timedelta(minutes=float(duration))
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{minutes}m {seconds}s'
    
# Helpers
def send_request_with_project_id(api_path: str, project_id: str, sort=False):
    
    url = f'{config.BACKEND_PROJECTS_FULL_PATH}/{api_path}'
    if sort:
        sort = request.args.get('sort', 'newer')
        params = {'project_id': project_id,
                'sort': sort}
    else:
        params = {'project_id': project_id}
        
    response = requests.get(url=url, params=params)
    if not response.status_code == 200:
        abort(500)
        
    return json.loads(response.text)

def get_divisi_range(divisi: list[dict]):
    
    general_count = 0
    for row in divisi:
        # possible number of staves
        for n in range(11):
            # determine the first staff which is None
            if not row[f'staff_{n+1}']:
                row_count = n
                if row_count > general_count:
                    general_count = n
                break

    
    return general_count

