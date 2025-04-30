from os import getenv

BACKEND_HOSTNAME = getenv('BACKEND_HOSTNAME', 'http://localhost')
BACKEND_PORT = getenv('BACKEND_PORT', '5000')  