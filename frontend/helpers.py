import jwt

from flask import request
from frontend import app

def is_authenticated():
    token = request.cookies.get('access_token_cookie')
    if not token:
        return False
    try:
        payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=[app.config['JWT_ALGORITHM']])
        print(payload)
        return True
    except jwt.InvalidTokenError:
        return False