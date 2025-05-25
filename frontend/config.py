from os import getenv


def set_env(key: str):
    env = getenv(key)
    if not env:
        raise ValueError(f'env variable {key} must be specified')
    return env


BACKEND_HOSTNAME = getenv('BACKEND_HOSTNAME', 'http://localhost')
BACKEND_PORT = getenv('BACKEND_PORT', '5000')
BACKEND_PROJECTS_PATH = getenv('BACKEND_PROJECTS', 'projects')
BACKEND_PROJECTS_FULL_PATH = f'{BACKEND_HOSTNAME}:{BACKEND_PORT}/{BACKEND_PROJECTS_PATH}'

AUTH_HOSTNAME = getenv('BACKEND_HOSTNAME', 'http://localhost')
AUTH_PORT = getenv('BACKEND_PORT', '5002')
AUTH_PATH = getenv('BACKEND_PROJECTS', 'api')
AUTH_PROJECTS_FULL_PATH = f'{AUTH_HOSTNAME}:{AUTH_PORT}/{AUTH_PATH}'


SECRET_KEY = set_env('SECRET_KEY')
JWT_SECRET_KEY = set_env('JWT_SECRET_KEY')
JWT_TOKEN_LOCATION = ['cookies']
