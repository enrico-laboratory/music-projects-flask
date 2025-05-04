from os import getenv
from dotenv import load_dotenv


def set_env_var(env: str, default: str=None):
    env = getenv(env, default)
    if not env:
        raise ValueError(f'{env} must be set')
    return env

load_dotenv('.env')

NOTION_API_TOKEN = set_env_var('NOTION_API_TOKEN')

MUSIC_PROJECT_SQLITE_DB_FOLDER = 'instance'
MUSIC_PROJECT_SQLITE_DB_FILENAME = 'music_projects.db'
MUSIC_PROJECTS_SQLITE_DB_URL = 'sqlite:///{folder}/{filename}'
MUSIC_PROJECT_SQLITE_DB_SAVE_LAST_BACKUP = False
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
