from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from utils import Notion
from db_builder import config as c
from db_builder.builder.music import MusicBuilder
from db_builder.builder import Builder, LocationBuilder, MusicProjectBuilder, ChoirBuilder, TaskBuilder, MusicBuilder, ContactBuilder, RoleBuilder, PartAllocationBuilder
from db_builder.db import ProjectBase, ChoirTable, LocationTable, MusicProjectTable, TaskTable, MusicTable, ContactTable, RoleTable, PartAllocationTable

def init_db() -> Session:
    
    Path(c.MUSIC_PROJECT_SQLITE_DB_FOLDER).mkdir(exist_ok=True)

    project_engine = create_engine(c.MUSIC_PROJECTS_SQLITE_DB_URL.format(
        folder=c.MUSIC_PROJECT_SQLITE_DB_FOLDER,
        filename=c.MUSIC_PROJECT_SQLITE_DB_FILENAME),
        echo=False)

    ProjectBase.metadata.create_all(project_engine)
    Session = sessionmaker(bind=project_engine)
    
    return Session()

