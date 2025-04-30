import logging
import json
import os
from pathlib import Path

from sqlalchemy.exc import SQLAlchemyError
from flask import Flask
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

from utils import Notion
from notion_db import config as c
from notion_db import (
    Builder,
    MusicProjectBuilder,
    ChoirBuilder,
    LocationBuilder,
    TaskBuilder,
    MusicBuilder,
    ContactBuilder,
    RoleBuilder,
    PartAllocationBuilder
)
from notion_db import (
    Base,
    ChoirTable,
    MusicProjectTable,
    LocationTable,
    TaskTable,
    MusicTable,
    ContactTable,
    RoleTable,
    PartAllocationTable
)


MUSIC_PROJECT_SQLITE_DB_FOLDER = 'instance/'
MUSIC_PROJECT_SQLITE_DB_FILENAME = 'music_projects.db'
MUSIC_PROJECTS_SQLITE_DB_URL = 'sqlite:///{folder}{filename}'

PATH_TO_JSON_DATABASE = 'database_json'
FROM_FILE = True
PRINT_TABLE_CHOIR = False
PRINT_TABLE_CONTACT = False
PRINT_TABLE_LOCATION = False
PRINT_TABLE_MUSIC = False
PRINT_TABLE_MUSIC_PROJECT = False
PRINT_TABLE_PART_ALLOCATION = False
PRINT_TABLE_ROLE = True
PRINT_TABLE_MUSIC_TASK = False

logging.basicConfig(format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

engine = create_engine(MUSIC_PROJECTS_SQLITE_DB_URL.format(
    folder=MUSIC_PROJECT_SQLITE_DB_FOLDER, filename=MUSIC_PROJECT_SQLITE_DB_FILENAME), echo=True)
db = SQLAlchemy()


def create_app(db_url=None) -> Flask:
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", MUSIC_PROJECTS_SQLITE_DB_URL.format(folder="", filename=MUSIC_PROJECT_SQLITE_DB_FILENAME))
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    return app


def init_db(app: Flask):

    db.init_app(app)

    with app.app_context():
        Base.metadata.create_all(engine)


def insert_row(app: Flask, table: any, **kargs):

    try:
        with app.app_context():
            row = table(**kargs)
            db.session.add(row)
            db.session.commit()

    except SQLAlchemyError as e:
        raise e

    return


def get_notion_database_from_file_or_api(notion_get_func, filename: str, from_file=False, path_to_json_database=PATH_TO_JSON_DATABASE) -> dict:

    if from_file:

        Path(path_to_json_database).mkdir(exist_ok=True)

        path = Path(path_to_json_database, filename)
        if path.is_file():

            with open(path, 'r') as f:
                database_dict = json.loads(f.read())

            return database_dict

        else:

            with open(path, 'w') as f:
                database_dict = notion_get_func()
                f.write(json.dumps(database_dict))

            return database_dict

    return notion_get_func()


def print_table(app: Flask, table: Base, title: str, print_table=False):

    if not print_table:
        return

    print(f'==== {title} ====')

    with app.app_context():
        response = db.session.query(table).all()
        for row in response:
            print(row)


def parse_tasks(tasks_dict: dict):

    excluded_list = []
    for i, page in enumerate(tasks_dict['results']):
        if not page['properties']['Type']['select']:
            excluded_list.append(i)
        else:
            if page['properties']['Type']['select']['name'] != 'Rehearsal' and page['properties']['Type']['select']['name'] != 'Concert':
                excluded_list.append(i)

    for index in reversed(excluded_list):

        del tasks_dict['results'][index]

    return tasks_dict


def get_foreign_key(app: Flask, notion_id: str, table) -> int:

    with app.app_context():
        row = db.session.query(table).filter_by(
            id_notion=notion_id).first()

    if not row:

        return None

    return row.id


def get_builder(builder_class: Builder, page: dict, ) -> Builder:

    try:
        builder_obj = builder_class(page)
    except ValueError as e:
        log.fatal(f"something went wrong creating the builder: {e}")
        exit(1)

    return builder_obj


def main():

    os.remove(
        f'{MUSIC_PROJECT_SQLITE_DB_FOLDER}{MUSIC_PROJECT_SQLITE_DB_FILENAME}')

    app = create_app()
    init_db(app)

    notion = Notion(c.NOTION_API_TOKEN)

    ### CHOIRS ###
    choirs_dict = get_notion_database_from_file_or_api(
        notion.get_choirs,
        'choir.json',
        from_file=FROM_FILE
    )
    for page in choirs_dict['results']:

        choir: ChoirBuilder = get_builder(ChoirBuilder, page)

        insert_row(app, ChoirTable, id_notion=choir.properties.id,
                   name=choir.properties.name)

    print_table(app, ChoirTable, "Choirs", print_table=PRINT_TABLE_CHOIR)

    ### CONTACT ###
    contacts_dict = get_notion_database_from_file_or_api(
        notion.get_contacts,
        'contacts.json',
        from_file=FROM_FILE)

    for page in contacts_dict['results']:

        contact: ContactBuilder = get_builder(ContactBuilder, page)

        insert_row(app,
                   ContactTable,
                   id_notion=contact.properties.id,
                   name=contact.properties.name,
                   role=contact.properties.role,
                   email1=contact.properties.email1,
                   email2=contact.properties.email2,
                   address=contact.properties.address,
                   phone=contact.properties.phone,
                   notes=contact.properties.notes,
                   voice=contact.properties.voice)

    print_table(app, ContactTable, "Table",
                print_table=PRINT_TABLE_CONTACT)

    ### LOCATIONS ###
    location_dict = get_notion_database_from_file_or_api(
        notion.get_locations,
        'location.json',
        from_file=FROM_FILE
    )

    for page in location_dict['results']:

        location: LocationBuilder = get_builder(LocationBuilder, page)

        insert_row(app,
                   LocationTable,
                   id_notion=location.properties.id,
                   name=location.properties.name,
                   city=location.properties.city,
                   address=location.properties.address,
                   purpose=location.properties.purpose)

    print_table(app, LocationTable, "Locations",
                print_table=PRINT_TABLE_LOCATION)

    ### MUSIC ###
    music_dict = get_notion_database_from_file_or_api(
        notion.get_music,
        'music.json',
        from_file=FROM_FILE)

    for page in music_dict['results']:

        music: MusicBuilder = get_builder(MusicBuilder, page)
        insert_row(app,
                   MusicTable,
                   id_notion=music.properties.id,
                   name=music.properties.name,
                   composer=music.properties.composer,
                   voices=music.properties.voices,
                   instruments=music.properties.instruments,
                   solo=music.properties.solo,
                   length=music.properties.length,
                   score=music.properties.score,
                   media=music.properties.media,
                   recording=music.properties.recording)

    print_table(app, MusicTable, "Music",
                print_table=PRINT_TABLE_MUSIC)

    ### MUSIC PROJECTS ###
    music_projects_dict = get_notion_database_from_file_or_api(
        notion.get_music_projects,
        'music_projects.json',
        from_file=FROM_FILE)

    for page in music_projects_dict['results']:

        music_project: MusicProjectBuilder = get_builder(
            MusicProjectBuilder, page)

        choir_id = get_foreign_key(app,
                                   music_project.properties.choir_id,
                                   ChoirTable)
        insert_row(app,
                   MusicProjectTable,
                   choir_id=choir_id,
                   id_notion=music_project.properties.id,
                   name=music_project.properties.name,
                   year=music_project.properties.year,
                   status=music_project.properties.status,
                   excerpt=music_project.properties.excerpt,
                   description=music_project.properties.description)

    print_table(app, MusicProjectTable, "Music Projects",
                print_table=PRINT_TABLE_MUSIC_PROJECT)

    ### PART ALLOCATION ###
    repertoire_dict = get_notion_database_from_file_or_api(
        notion.get_repertoire,
        'repertoire.json',
        from_file=FROM_FILE)

    for page in repertoire_dict['results']:

        part_allocation: PartAllocationBuilder = get_builder(
            PartAllocationBuilder, page)

        music_project_id = get_foreign_key(app,
                                           part_allocation.properties.music_project_id,
                                           MusicProjectTable)

        music_id = get_foreign_key(app,
                                   part_allocation.properties.music_id,
                                   MusicTable)
        insert_row(app,
                   PartAllocationTable,
                   name=part_allocation.properties.name,
                   music_id=music_id,
                   music_project_id=music_project_id,
                   staff_1=part_allocation.properties.staff_1,
                   staff_2=part_allocation.properties.staff_2,
                   staff_3=part_allocation.properties.staff_3,
                   staff_4=part_allocation.properties.staff_4,
                   staff_5=part_allocation.properties.staff_5,
                   staff_6=part_allocation.properties.staff_6,
                   staff_7=part_allocation.properties.staff_7,
                   staff_8=part_allocation.properties.staff_8,
                   staff_9=part_allocation.properties.staff_9,
                   staff_10=part_allocation.properties.staff_10,
                   staff_11=part_allocation.properties.staff_11,
                   staff_12=part_allocation.properties.staff_12,
                   notes=part_allocation.properties.notes,
                   selected=part_allocation.properties.selected)

    print_table(app, PartAllocationTable, "Part Allocation",
                print_table=PRINT_TABLE_PART_ALLOCATION)

    ### ROLE ###
    cast_dict = get_notion_database_from_file_or_api(
        notion.get_cast,
        'cast.json',
        from_file=FROM_FILE)

    for page in cast_dict['results']:

        role: RoleBuilder = get_builder(
            RoleBuilder, page)

        music_project_id = get_foreign_key(app,
                                           role.properties.music_project_id,
                                           MusicProjectTable)

        contact_id = get_foreign_key(app,
                                     role.properties.contact_id,
                                     ContactTable)

        insert_row(app,
                   RoleTable,
                   name=role.properties.name,
                   id_notion=role.properties.id,
                   music_project_id=music_project_id,
                   contact_id=contact_id,
                   note=role.properties.note,
                   status=role.properties.status)

    print_table(app, RoleTable, "Role",
                print_table=PRINT_TABLE_ROLE)

    ### TASKS ###
    tasks_dict_unparsed = get_notion_database_from_file_or_api(
        notion.get_tasks,
        'tasks.json',
        from_file=FROM_FILE)

    tasks_dict = parse_tasks(tasks_dict_unparsed)

    for page in tasks_dict['results']:

        task: TaskBuilder = get_builder(
            TaskBuilder, page)

        location_id = get_foreign_key(app,
                                      task.properties.location_id,
                                      LocationTable)

        music_project_id = get_foreign_key(app,
                                           task.properties.music_project_id,
                                           MusicProjectTable)

        insert_row(app,
                   TaskTable,
                   id_notion=task.properties.id,
                   name=task.properties.name,
                   start_date_time=task.properties.start_date_time,
                   end_date_time=task.properties.end_date_time,
                   type=task.properties.type,
                   music_project_id=music_project_id,
                   location_id=location_id)

    print_table(app, TaskTable, "Task table",
                print_table=PRINT_TABLE_MUSIC_TASK)


if __name__ == "__main__":
    main()
