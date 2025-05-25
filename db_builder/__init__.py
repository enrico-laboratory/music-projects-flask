from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

from utils import Notion
from db_builder import config as c
from db_builder.builder.music import MusicBuilder
from db_builder.builder import Builder, LocationBuilder, MusicProjectBuilder, ChoirBuilder, TaskBuilder, MusicBuilder, ContactBuilder, RoleBuilder, PartAllocationBuilder

def init_db(db_filename: str, base: DeclarativeBase) -> Session:
    
    Path(c.SQLITE_DB_FOLDER).mkdir(exist_ok=True)

    project_engine = create_engine(c.SQLITE_DB_URL.format(
        folder=c.SQLITE_DB_FOLDER,
        filename=db_filename),
        echo=False)

    base.metadata.create_all(project_engine)
    Session = sessionmaker(bind=project_engine)
    
    return Session()

