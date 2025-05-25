import json

import requests
from flask import Blueprint, render_template, flash, redirect, url_for, request, make_response

from flask_jwt_extended import jwt_required, set_access_cookies, unset_access_cookies, current_user

from frontend.forms import RegistrationFrom, LoginForm
from frontend.config import AUTH_PROJECTS_FULL_PATH
from frontend import jwt

blp = Blueprint('main', __name__)


@blp.route('/')
def home():
    return render_template('home.html.jinja')


@blp.route('/login', methods=['GET', 'POST'])
def login():

    title = 'Login'
    form = LoginForm()

    if form.validate_on_submit():
        url = f"{AUTH_PROJECTS_FULL_PATH}/login"
        headers = {"content-type": "application/json"}
        body = {"email": form.email.data, "password": form.password.data}
        response = requests.post(
            url=url, headers=headers, data=json.dumps(body))

        if response.status_code == 200:
            flash('You are logged in!', 'success')
            token = json.loads(response.text)['access_token']
            resp = make_response(redirect(url_for('main.home')))
            set_access_cookies(resp, encoded_access_token=token)
            
            return resp
        
        if response.status_code == 422:
            log.error(response.text)

        if response.status_code == 401:
            flash('email and password combination not valid', 'danger')

        if response.status_code == 500:
            flash(
                f'Something went wrong with user registration, try again later', 'warning')

    return render_template('login.html.jinja',
                           title=title,
                           form=form)

@blp.route('/logout')
def logout():
    if "access_token_cookie" in request.cookies:  
        resp = make_response(redirect(url_for('main.home')))
        unset_access_cookies(response=resp)
        flash('You have been logged out!', 'success')
        return resp
    flash('you are not logged in', 'warning')
    return redirect(url_for('main.home'))
    


@blp.route('/register', methods=['GET', 'POST'])
def register():

    title = 'Register'
    form = RegistrationFrom()

    if form.validate_on_submit():

        url = f"{AUTH_PROJECTS_FULL_PATH}/register"
        headers = {"content-type": "application/json"}
        body = {"email": form.email.data, "password": form.password.data}
        response = requests.post(
            url=url, headers=headers, data=json.dumps(body))

        if response.status_code == 201:
            flash(f'Your accoun as been created', 'success')
            return redirect(url_for('main.login'))

        if response.status_code == 409:
            flash(f'account with email {form.email} already exists!', 'danger')

        if response.status_code == 500:
            flash(
                f'Something went wrong with user registration, try again later', 'warning')

    return render_template('register.html.jinja',
                           title=title,
                           form=form)

@jwt.unauthorized_loader
def custom_unauthorized_response(_err):
    flash('you are not authorized to visit this page. Please log in', 'danger')
    return redirect(url_for('main.login'))