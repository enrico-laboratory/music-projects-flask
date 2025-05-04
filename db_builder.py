import logging

from utils import Notion
from db_builder import init_db
from db_builder import config as c
from db_builder.notion import NotionDatabase
from db_builder.prjoject_db import delete_database_if_exists, backup_database_if_exist
from db_builder.prjoject_db import (
    ChoirDB,
    ContactDB,
    LocationDB,
    MusicDB
)


logging.basicConfig(format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


if __name__ == "__main__":
    
    db_path = f'{c.MUSIC_PROJECT_SQLITE_DB_FOLDER}/{c.MUSIC_PROJECT_SQLITE_DB_FILENAME}'
    n = Notion(c.NOTION_API_TOKEN)

    log.debug(f'Backup db and save last backup is {c.MUSIC_PROJECT_SQLITE_DB_SAVE_LAST_BACKUP}')
    backup_database_if_exist(
        db_path,
        save_last_backup=c.MUSIC_PROJECT_SQLITE_DB_SAVE_LAST_BACKUP)
    
    log.debug('Delete existing database')
    delete_database_if_exists(db_path)
    
    log.debug('Init Dabatase')
    project_session = init_db()
    
    log.debug('Get Notion Choir Database')    
    choir_notion_dict = NotionDatabase(
        n.get_choirs, 'choirs', c.PATH_TO_JSON_DATABASE,
        generate_from_file= True 
    ).data
    
    log.debug('Get Notion Contact Database')    
    contact_notion_dict = NotionDatabase(
        n.get_contacts, 'contacts', c.PATH_TO_JSON_DATABASE,
        generate_from_file= True 
    ).data
    
    log.debug('Get Notion Location Database')    
    location_notion_dict = NotionDatabase(
        n.get_locations, 'locations', c.PATH_TO_JSON_DATABASE,
        generate_from_file= True 
    ).data

    log.debug('Get Notion Music Database')    
    music_notion_dict = NotionDatabase(
        n.get_music, 'music', c.PATH_TO_JSON_DATABASE,
        generate_from_file= True 
    ).data
    
    log.debug('Insert row in Choir Database')
    choir_db = ChoirDB(
        project_session, db_path,
        notion_db=choir_notion_dict)
    
    choir_db.insert_data_in_db()
    # choir_db.print_table()

    log.debug('Insert row in Contact Database')
    contact_db = ContactDB(
        project_session, db_path,
        notion_db=contact_notion_dict)
    
    contact_db.insert_data_in_db()
    # contact_db.print_table()
    
    log.debug('Insert row in Location Database')
    location_db = LocationDB(
        project_session, db_path,
        notion_db=location_notion_dict)
    
    location_db.insert_data_in_db()
    # location_db.print_table()

    log.debug('Insert row in Music Database')
    music_db = MusicDB(
        project_session, db_path,
        notion_db=music_notion_dict)
    
    music_db.insert_data_in_db()
    # music_db.print_table()
