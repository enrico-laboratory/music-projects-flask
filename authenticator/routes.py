from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token

from models.auth_tables import UserTable
from authenticator.schema import UserSchemaRegister, UserSchemaLogin
from authenticator import db

blp = Blueprint("Authenticator",
                __name__,
                description='Api endpoint for authenticate')


@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserSchemaLogin)
    def post(self, user_data):

        user = db.session.query(UserTable).filter(
            UserTable.email == user_data['email']
        ).first()

        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            return {'access_token': access_token, 'refresh_token': refresh_token }

        abort(401, message="invalid credentials")


@blp.route("/register")
class UserRegister(MethodView):

    @blp.arguments(UserSchemaRegister)
    def post(self, user_data):
        if db.session.query(UserTable).filter(UserTable.email == user_data['email']).first():
            abort(
                409, message=f"user with email {user_data['email']} already exists")

        user = UserTable(
            username=user_data['username'],
            email=user_data['email'],
            password=pbkdf2_sha256.hash(user_data['password']),
            role=user_data['role']
        )

        db.session.add(user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201


@blp.route("/user/<int:user_id>")
class User(MethodView):

    @blp.response(200, UserSchemaRegister)
    def get(self, user_id):
        user = db.get_or_404(UserTable, user_id)
        return user

    def delete(self, user_id):
        user = db.get_or_404(UserTable, user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "user deleted"}, 200


@blp.route("/users")
class UserByEmail(MethodView):

    @blp.response(200, UserSchemaRegister(many=True))
    def get(self):
        email = request.args.get('email', "")
        username = request.args.get('username', '')
        if not email and not username:
            users = db.session.query(UserTable).all()
        if email:
            users = db.session.query(UserTable).filter(
                UserTable.email == email
            ).all()
        # if username:
        #     users = db.session.query(UserTable).filter(
        #         UserTable.username == username
        #     ).all()

        return users
