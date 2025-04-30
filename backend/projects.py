from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from sqlalchemy.exc import SQLAlchemyError


from backend import db
from backend.schemas import (
    PlainChoirSchema,
    PlainContactSchema,
    PlainLocationSchema,
    PlainMusicSchema,
    PlainMusicProjectSchema,
    PlainTaskSchema
)

from notion_db import (
    ChoirTable,
    ContactTable,
    LocationTable,
    MusicTable,
    MusicProjectTable,
    TaskTable,
)

blp = Blueprint("Projects", __name__, description="Operations on items")


@blp.route('/choir/<int:choir_id>')
class Choir(MethodView):

    @blp.response(200, PlainChoirSchema)
    def get(self, choir_id):
        choir = db.get_or_404(ChoirTable, choir_id)
        return choir


@blp.route('/choir')
class ChoirList(MethodView):

    @blp.response(200, PlainChoirSchema(many=True))
    def get(self):
        return db.session.query(ChoirTable).all()

    def post(self, choir_data):
        pass


@blp.route('/contact/<int:contact_id>')
class Contact(MethodView):

    @blp.response(200, PlainContactSchema)
    def get(self, contact_id):
        choir = db.get_or_404(ContactTable, contact_id)
        return choir


@blp.route('/contact')
class ContactList(MethodView):

    @blp.response(200, PlainContactSchema(many=True))
    def get(self):
        return db.session.query(ContactTable).all()


@blp.route('/location/<int:location_id>')
class Location(MethodView):

    @blp.response(200, PlainLocationSchema)
    def get(self, location_id):
        choir = db.get_or_404(LocationTable, location_id)
        return choir


@blp.route('/location')
class LocationList(MethodView):

    @blp.response(200, PlainLocationSchema(many=True))
    def get(self):
        return db.session.query(LocationTable).all()

@blp.route('/music/<int:music_id>')
class Music(MethodView):

    @blp.response(200, PlainMusicSchema)
    def get(self, music_id):
        choir = db.get_or_404(MusicTable, music_id)
        return choir


@blp.route('/music')
class MusicList(MethodView):

    @blp.response(200, PlainMusicSchema(many=True))
    def get(self):
        return db.session.query(MusicTable).all()
    

@blp.route('/music_project/<int:music_project_id>')
class MusicProject(MethodView):

    @blp.response(200, PlainMusicProjectSchema)
    def get(self, music_project_id):
        music_project = db.get_or_404(MusicProjectTable, music_project_id)
        return music_project


@blp.route('/music_project')
class MusicProjectList(MethodView):

    @blp.response(200, PlainMusicProjectSchema(many=True))
    def get(self):
        return db.session.query(MusicProjectTable).all()


@blp.route('/task/<int:task_id>')
class Task(MethodView):

    @blp.response(200, PlainTaskSchema)
    def get(self, task_id):
        return db.get_or_404(TaskTable, task_id)


@blp.route('/task')
class TaskList(MethodView):

    @blp.response(200, PlainTaskSchema(many=True))
    def get(self):

        filter = request.args.get('filter', "")
        sort = request.args.get('sort', "newer")

        if sort == "newer":
            order_by = TaskTable.start_date_time.desc()
        else:
            order_by = TaskTable.start_date_time.asc()

        try:
            if not filter:
                result = db.session.query(TaskTable).order_by(order_by).all()
            else:
                result = db.session.query(TaskTable).join(MusicProjectTable).where(
                    MusicProjectTable.name == filter).order_by(order_by).all()

        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return result

    def post(self, choir_data):
        pass
