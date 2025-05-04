import json

import requests
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from frontend.config import AUTH_PROJECTS_FULL_PATH


class RegistrationFrom(FlaskForm):

    username = StringField('Username',
                           render_kw={"placeholder": "Username"},
                           validators=[DataRequired(),
                                       Length(min=2, max=20)])
    email = StringField('Email',
                        render_kw={"placeholder": "Email"},
                        validators=[
                            DataRequired(),
                            Email()])
    password = PasswordField('Password',
                             render_kw={"placeholder": "Password"},
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     render_kw={
                                         "placeholder": "Confirm Password"},
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        url = f"{AUTH_PROJECTS_FULL_PATH}/users"
        response = requests.get(url=url, params={'email': email})
        if json.loads(response.text):
            raise ValidationError(
                'That email is taken. Please choose a different one')


class LoginForm(FlaskForm):

    email = StringField('Email',
                        render_kw={"placeholder": "Email"},
                        validators=[
                            DataRequired(),
                            Email()])
    password = PasswordField('Password',
                             render_kw={"placeholder": "Password"},
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
