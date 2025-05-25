import jwt
from functools import wraps

from flask import session, redirect, url_for, flash

from frontend import app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = session.get('token')
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            return f(*args, **kwargs)
        except Exception as e:
            print(e)
            flash("you need to login to visit this page", 'danger')
               
            return redirect(url_for('main.login'))
            # Response(json.dumps({"message": "Unauthorized user"}), 401, headers=headers)
    return decorated