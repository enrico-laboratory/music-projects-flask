import logging

from utils import Notion
from db_builder import init_db
from db_builder import config as c
from db_builder.notion import NotionDatabase
from db_builder import ProjectBase, AuthBase
from db_builder.prjoject_db import delete_database_if_exists, backup_database_if_exist
from db_builder.prjoject_db import (
    ChoirDB,
    ContactDB,
    LocationDB,
    MusicDB,
    MusicProjectDB,
    PartAllocationDB,
    RoleDB,
    TaskDB
)


logging.basicConfig(format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


if __name__ == "__main__":
    

    n = Notion(c.NOTION_API_TOKEN)

    log.info(f'Backup db and save last backup is {c.MUSIC_PROJECT_SQLITE_DB_SAVE_LAST_BACKUP}')
    backup_database_if_exist(
        c.MUSIC_PROJECT_DB_PATH,
        save_last_backup=c.MUSIC_PROJECT_SQLITE_DB_SAVE_LAST_BACKUP)
    
    log.info('Delete existing Music project database')
    delete_database_if_exists(c.MUSIC_PROJECT_DB_PATH)

    log.info(f'Backup db and save last backup is {c.AUTH_SQLITE_DB_SAVE_LAST_BACKUP}')
    backup_database_if_exist(
        c.AUTH_DB_PATH,
        save_last_backup=c.AUTH_SQLITE_DB_SAVE_LAST_BACKUP)
    
    log.info('Delete existing Music project database')
    delete_database_if_exists(c.AUTH_DB_PATH)    
    
    log.info('Init Projects Dabatase')
    project_session = init_db(c.MUSIC_PROJECT_SQLITE_DB_FILENAME, ProjectBase)

    log.info('Init Auth Dabatase')
    auth_session = init_db(c.AUTH_SQLITE_DB_FILENAME, AuthBase)
      
    log.info('Get Notion Choir Database')    
    choir_notion_dict = NotionDatabase(
        n.get_choirs, 'choirs', c.PATH_TO_JSON_DATABASE,
        generate_from_file= True 
    ).data
    
    log.info('Get Notion Contact Database')    
    contact_notion_dict = NotionDatabase(
        n.get_contacts, 'contacts', c.PATH_TO_JSON_DATABASE,
        generate_from_file= True 
    ).data
    
    log.info('Get Notion Location Database')    
    location_notion_dict = NotionDatabase(
        n.get_locations, 'locations', c.PATH_TO_JSON_DATABASE,
        generate_from_file= True 
    ).data

    log.info('Get Notion Music Database')    
    music_notion_dict = NotionDatabase(
        n.get_music, 'music', c.PATH_TO_JSON_DATABASE,
        generate_from_file= True 
    ).data

    log.info('Get Notion Music Projects Database')    
    music_projects_notion_dict = NotionDatabase(
        n.get_music_projects, 'music_projects', c.PATH_TO_JSON_DATABASE,
        generate_from_file= True 
    ).data
    
    log.info('Get Notion Repertoire Database')    
    repertoire_notion_dict = NotionDatabase(
        n.get_repertoire, 'repertoire', c.PATH_TO_JSON_DATABASE,
        generate_from_file= True 
    ).data
    
    log.info('Get Notion Cast Database')    
    cast_notion_dict = NotionDatabase(
        n.get_cast, 'cast', c.PATH_TO_JSON_DATABASE,
        generate_from_file= True 
    ).data

    log.info('Get Notion Tasks Database')    
    tasks_notion_dict = NotionDatabase(
        n.get_tasks, 'tasks', c.PATH_TO_JSON_DATABASE,
        generate_from_file= True 
    ).data    


    log.info('Insert row in Choir Database')
    choir_db = ChoirDB(
        project_session, c.MUSIC_PROJECT_DB_PATH,
        notion_db=choir_notion_dict)
    
    choir_db.insert_data_in_db()
    # choir_db.print_table()

    log.info('Insert row in Contact Database')
    contact_db = ContactDB(
        project_session, c.MUSIC_PROJECT_DB_PATH,
        notion_db=contact_notion_dict)
    
    contact_db.insert_data_in_db()
    # contact_db.print_table()
    
    log.info('Insert row in Location Database')
    location_db = LocationDB(
        project_session, c.MUSIC_PROJECT_DB_PATH,
        notion_db=location_notion_dict)
    
    location_db.insert_data_in_db()
    # location_db.print_table()

    log.info('Insert row in Music Database')
    music_db = MusicDB(
        project_session, c.MUSIC_PROJECT_DB_PATH,
        notion_db=music_notion_dict)
    
    music_db.insert_data_in_db()
    # music_db.print_table()

    log.info('Insert row in Music Project Database')
    music_projects_db = MusicProjectDB(
        project_session, c.MUSIC_PROJECT_DB_PATH,
        notion_db=music_projects_notion_dict)
    
    music_projects_db.insert_data_in_db()
    # music_projects_db.print_table()

    log.info('Insert row in Part Allocation Database')
    part_allocation_db = PartAllocationDB(
        project_session, c.MUSIC_PROJECT_DB_PATH,
        notion_db=repertoire_notion_dict)
    
    part_allocation_db.insert_data_in_db()
    # part_allocation_db.print_table()

    log.info('Insert row in Role Database')
    role_db = RoleDB(
        project_session, c.MUSIC_PROJECT_DB_PATH,
        notion_db=cast_notion_dict)
    
    role_db.insert_data_in_db()
    # role_db.print_table()

    log.info('Insert row in Task Database')
    task_db = TaskDB(
        project_session, c.MUSIC_PROJECT_DB_PATH,
        notion_db=tasks_notion_dict)
    
    task_db.insert_data_in_db()
    # task_db.print_table()
    