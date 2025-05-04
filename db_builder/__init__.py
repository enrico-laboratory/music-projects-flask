import logging
import json
import os
from pathlib import Path

from sqlalchemy.exc import SQLAlchemyError
from flask import Flask
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

from utils import Notion
from db_builder import config as c
from db_builder.builder.music import MusicBuilder
from db_builder.builder import Builder, LocationBuilder, MusicProjectBuilder, ChoirBuilder, TaskBuilder, MusicBuilder, ContactBuilder, RoleBuilder, PartAllocationBuilder
from db_builder.db import ProjectBase, ChoirTable, LocationTable, MusicProjectTable, TaskTable, MusicTable, ContactTable, RoleTable, PartAllocationTable

def create_app(db_url=None) -> Flask:
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home/eruggieri/repo/music-projects-flask/instance/music_projects.db"
    # app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        # "DATABASE_URL", c.MUSIC_PROJECTS_SQLITE_DB_URL.format(folder="", filename=c.MUSIC_PROJECT_SQLITE_DB_FILENAME))
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    return app


def init_db(app: Flask) -> SQLAlchemy:
    
    project_engine = create_engine(c.MUSIC_PROJECTS_SQLITE_DB_URL.format(
        folder=c.MUSIC_PROJECT_SQLITE_DB_FOLDER,
        filename=c.MUSIC_PROJECT_SQLITE_DB_FILENAME),
        echo=False,
        pool_pre_ping=True)
    
    db = SQLAlchemy()
    db.init_app(app)

    with app.app_context():
        print(db.get_engine())
        ProjectBase.metadata.create_all(project_engine)
        
    return db
