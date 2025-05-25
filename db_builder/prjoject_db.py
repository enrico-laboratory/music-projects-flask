from pathlib import Path
import shutil
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from db_builder import (
    Builder,
    MusicProjectBuilder,
    ChoirBuilder,
    LocationBuilder,
    TaskBuilder,
    MusicBuilder,
    ContactBuilder,
    RoleBuilder,
    PartAllocationBuilder
)
from models.project_tables import (
    ProjectBase,
    ChoirTable,
    MusicProjectTable,
    LocationTable,
    TaskTable,
    MusicTable,
    ContactTable,
    RoleTable,
    PartAllocationTable
)


def backup_database_if_exist(database_path: str, save_last_backup=False) -> bool:

    backup_ext = '.db.bak'
    now = datetime.now().strftime("%y%m%d-%H%M%S")
    backup_ext_now = f'{backup_ext}.{now}'
    database = Path(database_path)
    database_backup = database.with_suffix(backup_ext)
    database_backup_now = database.with_suffix(backup_ext_now)

    if database.is_file():
        if save_last_backup and database_backup.is_file():
            shutil.copy2(database_backup, database_backup_now)
        shutil.copy2(database, database_backup)
        return True

    return False


def delete_database_if_exists(database_path: str):

    database = Path(database_path)

    if database.is_file():
        database.unlink()


class ProjectNotionToDB:

    def __init__(self,
                 db_session: Session,
                 database_path: str,
                 notion_db: dict,
                 table: ProjectBase,
                 builder: Builder):

        self.db_session = db_session
        self.database_path = database_path
        self.notion_db = notion_db
        self.table = table
        self.builder = builder

    def get_builder(self, builder_class: Builder, page: dict, ) -> Builder:

        try:
            builder_obj = builder_class(page)
        except ValueError as e:
            raise ValueError(e)

        return builder_obj

    def insert_row(self, table: any, **kargs):

        try:
            row = table(**kargs)
            self.db_session.add(row)
            self.db_session.commit()

        except SQLAlchemyError as e:
            raise e

        return

    def get_foreign_key(self, notion_id: str, table) -> int:

        row = self.db_session.query(table).filter_by(
            id_notion=notion_id).first()

        if not row:

            return None

        return row.id

    def print_table(self, title: str = ""):

        if title:
            print(f'==== {title} ====')

        response = self.db_session.query(self.table).all()
        for row in response:
            print(row)


class ChoirDB(ProjectNotionToDB):

    def __init__(self,
                 db_session: Session,
                 database_path: str,
                 notion_db: dict):
        super().__init__(db_session, database_path, notion_db, ChoirTable, ChoirBuilder)

    def insert_data_in_db(self):

        for page in self.notion_db['results']:

            choir: Builder = self.get_builder(self.builder, page)

            self.insert_row(self.table,
                            id_notion=choir.properties.id,
                            name=choir.properties.name)


class ContactDB(ProjectNotionToDB):

    def __init__(self,
                 db_session: Session,
                 database_path: str,
                 notion_db: dict):
        super().__init__(db_session, database_path, notion_db, ContactTable, ContactBuilder)

    def insert_data_in_db(self):

        for page in self.notion_db['results']:

            contact: Builder = self.get_builder(self.builder, page)

            self.insert_row(self.table,
                            id_notion=contact.properties.id,
                            name=contact.properties.name,
                            role=contact.properties.role,
                            email1=contact.properties.email1,
                            email2=contact.properties.email2,
                            address=contact.properties.address,
                            phone=contact.properties.phone,
                            notes=contact.properties.notes,
                            voice=contact.properties.voice)


class LocationDB(ProjectNotionToDB):

    def __init__(self,
                 db_session: Session,
                 database_path: str,
                 notion_db: dict):
        super().__init__(db_session, database_path,
                         notion_db, LocationTable, LocationBuilder)

    def insert_data_in_db(self):

        for page in self.notion_db['results']:

            builder: Builder = self.get_builder(self.builder, page)

            self.insert_row(self.table,
                            id_notion=builder.properties.id,
                            name=builder.properties.name,
                            city=builder.properties.city,
                            address=builder.properties.address,
                            purpose=builder.properties.purpose)


class MusicDB(ProjectNotionToDB):

    def __init__(self,
                 db_session: Session,
                 database_path: str,
                 notion_db: dict):
        super().__init__(db_session, database_path, notion_db, MusicTable, MusicBuilder)

    def insert_data_in_db(self):

        for page in self.notion_db['results']:

            builder: Builder = self.get_builder(self.builder, page)

            self.insert_row(self.table,
                            id_notion=builder.properties.id,
                            name=builder.properties.name,
                            composer=builder.properties.composer,
                            voices=builder.properties.voices,
                            instruments=builder.properties.instruments,
                            solo=builder.properties.solo,
                            length=builder.properties.length,
                            score=builder.properties.score,
                            media=builder.properties.media,
                            recording=builder.properties.recording)


class MusicProjectDB(ProjectNotionToDB):

    def __init__(self,
                 db_session: Session,
                 database_path: str,
                 notion_db: dict):
        super().__init__(db_session, database_path, notion_db,
                         MusicProjectTable, MusicProjectBuilder)

    def insert_data_in_db(self):

        for page in self.notion_db['results']:

            builder: Builder = self.get_builder(self.builder, page)

            choir_id = self.get_foreign_key(builder.properties.choir_id,
                                            ChoirTable)
            self.insert_row(self.table,
                            choir_id=choir_id,
                            id_notion=builder.properties.id,
                            name=builder.properties.name,
                            year=builder.properties.year,
                            status=builder.properties.status,
                            excerpt=builder.properties.excerpt,
                            description=builder.properties.description)


class PartAllocationDB(ProjectNotionToDB):

    def __init__(self,
                 db_session: Session,
                 database_path: str,
                 notion_db: dict):
        super().__init__(db_session, database_path, notion_db,
                         PartAllocationTable, PartAllocationBuilder)

    def insert_data_in_db(self):

        for page in self.notion_db['results']:

            builder: Builder = self.get_builder(self.builder, page)

            music_project_id = self.get_foreign_key(builder.properties.music_project_id,
                                                    MusicProjectTable)

            music_id = self.get_foreign_key(builder.properties.music_id,
                                            MusicTable)
            self.insert_row(self.table,
                            name=builder.properties.name,
                            music_id=music_id,
                            music_project_id=music_project_id,
                            staff_1=builder.properties.staff_1,
                            staff_2=builder.properties.staff_2,
                            staff_3=builder.properties.staff_3,
                            staff_4=builder.properties.staff_4,
                            staff_5=builder.properties.staff_5,
                            staff_6=builder.properties.staff_6,
                            staff_7=builder.properties.staff_7,
                            staff_8=builder.properties.staff_8,
                            staff_9=builder.properties.staff_9,
                            staff_10=builder.properties.staff_10,
                            staff_11=builder.properties.staff_11,
                            staff_12=builder.properties.staff_12,
                            notes=builder.properties.notes,
                            selected=builder.properties.selected)


class RoleDB(ProjectNotionToDB):

    def __init__(self,
                 db_session: Session,
                 database_path: str,
                 notion_db: dict):
        super().__init__(db_session, database_path, notion_db,
                         RoleTable, RoleBuilder)

    def insert_data_in_db(self):

        for page in self.notion_db['results']:

            builder: Builder = self.get_builder(self.builder, page)

            music_project_id = self.get_foreign_key(builder.properties.music_project_id,
                                                    MusicProjectTable)

            contact_id = self.get_foreign_key(builder.properties.contact_id,
                                              ContactTable)
            self.insert_row(self.table,
                            name=builder.properties.name,
                            id_notion=builder.properties.id,
                            music_project_id=music_project_id,
                            contact_id=contact_id,
                            note=builder.properties.note,
                            status=builder.properties.status)


class TaskDB(ProjectNotionToDB):

    def __init__(self,
                 db_session: Session,
                 database_path: str,
                 notion_db: dict):
        super().__init__(db_session, database_path, notion_db,
                         TaskTable, TaskBuilder)

    def __parse_tasks(self, tasks_dict: dict):

        excluded_list = []
        for i, page in enumerate(tasks_dict['results']):
            if not page['properties']['Type']['select']:
                excluded_list.append(i)
            else:
                if page['properties']['Type']['select']['name'] != 'Rehearsal' and page['properties']['Type']['select']['name'] != 'Concert':
                    excluded_list.append(i)

        for index in reversed(excluded_list):

            del tasks_dict['results'][index]

        return tasks_dict
    
    def insert_data_in_db(self):
        
        parsed_notion_task_db = self.__parse_tasks(self.notion_db)
        for page in parsed_notion_task_db['results']:

            builder: Builder = self.get_builder(self.builder, page)

            music_project_id = self.get_foreign_key(builder.properties.music_project_id,
                                                    MusicProjectTable)

            location_id = self.get_foreign_key(builder.properties.location_id,
                                               LocationTable)
            self.insert_row(self.table,
                            id_notion=builder.properties.id,
                            name=builder.properties.name,
                            start_date_time=builder.properties.start_date_time,
                            end_date_time=builder.properties.end_date_time,
                            type=builder.properties.type,
                            music_project_id=music_project_id,
                            location_id=location_id)
