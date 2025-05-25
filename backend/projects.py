import logging

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import verify_jwt_in_request

from backend import db
from backend.schemas import (
    PlainChoirSchema,
    PlainContactSchema,
    PlainLocationSchema,
    PlainMusicSchema,
    PlainMusicProjectSchema,
    PlainPartAllocationSchema,
    PlainRoleSchema,
    PlainTaskSchema
)

from models.project_tables import (
    ProjectBase,
    ChoirTable,
    ContactTable,
    LocationTable,
    MusicTable,
    MusicProjectTable,
    PartAllocationTable,
    RoleTable,
    TaskTable,
)

log = logging.getLogger(__name__)

blp = Blueprint("Projects", __name__, description="Operations on items")

@blp.before_request
def require_jwt_for_all_requests():
    verify_jwt_in_request()

@blp.route('/choir/<int:choir_id>')
class Choir(MethodView):

    @blp.response(200, PlainChoirSchema)
    def get(self, choir_id):
        return get_single_item_by_id(ChoirTable, choir_id)


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
        return get_single_item_by_id(ContactTable, contact_id)


@blp.route('/contact')
class ContactList(MethodView):

    @blp.response(200, PlainContactSchema(many=True))
    def get(self):
        return db.session.query(ContactTable).all()


@blp.route('/location/<int:location_id>')
class Location(MethodView):

    @blp.response(200, PlainLocationSchema)
    def get(self, location_id):
        return get_single_item_by_id(LocationTable, location_id)


@blp.route('/location')
class LocationList(MethodView):

    @blp.response(200, PlainLocationSchema(many=True))
    def get(self):
        return db.session.query(LocationTable).all()


@blp.route('/music/<int:music_id>')
class Music(MethodView):

    @blp.response(200, PlainMusicSchema)
    def get(self, music_id):
        return get_single_item_by_id(MusicTable, music_id)


@blp.route('/music')
class MusicList(MethodView):

    @blp.response(200, PlainMusicSchema(many=True))
    def get(self):
        return db.session.query(MusicTable).all()


@blp.route('/music_project/<int:music_project_id>')
class MusicProject(MethodView):

    @blp.response(200, PlainMusicProjectSchema)
    def get(self, music_project_id):
        return get_single_item_by_id(MusicProjectTable, music_project_id)


@blp.route('/music_project')
class MusicProjectList(MethodView):

    @blp.response(200, PlainMusicProjectSchema(many=True))
    def get(self):
        return db.session.query(MusicProjectTable).all()


@blp.route('/part_allocation/<int:part_allocation_id>')
class PartAllocation(MethodView):

    @blp.response(200, PlainPartAllocationSchema)
    def get(self, part_allocation_id):
        return get_single_item_by_id(PartAllocationTable, part_allocation_id)


@blp.route('/part_allocation')
class PartAllocationList(MethodView):

    @blp.response(200, PlainPartAllocationSchema(many=True))
    def get(self):
        return get_list_by_project_id(PartAllocationTable)


@blp.route('/role/<int:role_id>')
class Role(MethodView):

    @blp.response(200, PlainRoleSchema)
    def get(self, role_id):
        return get_single_item_by_id(RoleTable, role_id)



@blp.route('/role')
class RoleLIst(MethodView):

    @blp.response(200, PlainRoleSchema(many=True))
    def get(self):
        return get_list_by_project_id(RoleTable)


@blp.route('/task/<int:task_id>')
class Task(MethodView):

    @blp.response(200, PlainTaskSchema)
    def get(self, task_id):
        return get_single_item_by_id(TaskTable, task_id)


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
                print('here')
            else:
                result = db.session.query(TaskTable).join(MusicProjectTable).where(
                    MusicProjectTable.id == filter).order_by(order_by).all()

        except SQLAlchemyError as e:
            log.error(e)
            abort(500, message="An error occurred creating the store.")

        return result

    def post(self, choir_data):
        pass


# Helpers
def get_list_by_project_id(table):

    project_id = request.args.get('project_id', "")

    try:
        if not project_id:
            result = db.session.query(table).all()
        else:
            result = db.session.query(table).join(MusicProjectTable).where(
                MusicProjectTable.id == project_id).all()
    except SQLAlchemyError as e:
        log.error(e)
        abort(500, message="An internal error occurred. Please try again later")

    return result

def get_single_item_by_id(table: ProjectBase, id: int):
    try:
        response = db.get_or_404(table, id)
    except SQLAlchemyError as e:
        log.error(e)
        abort(500, message="An internal error occurred. Please try again later")
    return response    