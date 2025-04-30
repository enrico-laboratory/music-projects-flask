from os import getenv
from dotenv import load_dotenv


def set_env_var(env: str, default: str=None):
    env = getenv(env, default)
    if not env:
        raise ValueError(f'{env} must be set')
    return env

load_dotenv('.env')
NOTION_API_TOKEN = set_env_var('NOTION_API_TOKEN')

