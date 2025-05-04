import logging

from utils import Notion
from db_builder import config as c
from db_builder.prjoject_db import delete_database_if_exists, backup_database_if_exist
from db_builder.prjoject_db import (
    ChoirDB
)
from db_builder import init_db, create_app
from db_builder.notion import NotionDatabase


logging.basicConfig(format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


if __name__ == "__main__":
    db_path = f'{c.MUSIC_PROJECT_SQLITE_DB_FOLDER}/{c.MUSIC_PROJECT_SQLITE_DB_FILENAME}'
    n = Notion(c.NOTION_API_TOKEN)

    log.debug('Create Flask app')
    app = create_app()

    log.debug(f'Backup db and save last backup is {c.MUSIC_PROJECT_SQLITE_DB_SAVE_LAST_BACKUP}')
    backup_database_if_exist(
        db_path,
        save_last_backup=c.MUSIC_PROJECT_SQLITE_DB_SAVE_LAST_BACKUP)
    
    log.debug('Delete existing database')
    delete_database_if_exists(db_path)
    
    log.debug('Init Dabatase')
    db = init_db(app)
    
    path_to_json_database=c.PATH_TO_JSON_DATABASE
    
    choir_notion_dict = NotionDatabase(
        n.get_choirs, 'choirs', path_to_json_database,
        generate_from_file= True 
    ).data
    
    choir_db = ChoirDB(
        app, db, db_path,
        notion_db=choir_notion_dict)
    
    choir_db.insert_data_in_db()
    choir_db.print_table()
    
    
