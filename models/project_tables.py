from datetime import datetime

from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, Boolean, Enum
from typing import Optional
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
from sqlalchemy.orm import Mapped

from models.enums import UserProjectRoleEnum


# TODO Replace values with ENUM

class ProjectBase(DeclarativeBase):
    pass


class ChoirTable(ProjectBase):
    __tablename__ = 'choir'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_notion: Mapped[Optional[str]] = mapped_column(String(36))
    name: Mapped[str] = mapped_column(String(30), unique=True)

    def __repr__(self) -> str:
        return f"ChoirTable(id={self.id!r}, id_notion={self.id_notion!r}, name={self.name!r})"


class ContactTable(ProjectBase):
    __tablename__ = 'contacts'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_notion: Mapped[Optional[str]] = mapped_column(String(36))
    name: Mapped[str] = mapped_column(String(30))
    role: Mapped[str] = mapped_column(String(30))
    email1: Mapped[str] = mapped_column(String())
    email2: Mapped[Optional[str]] = mapped_column(String())
    address: Mapped[Optional[str]] = mapped_column(String())
    phone: Mapped[Optional[str]] = mapped_column(String())
    notes: Mapped[Optional[str]] = mapped_column(String())
    voice: Mapped[Optional[str]] = mapped_column(String())

    def __repr__(self) -> str:
        return f"ContactTable(id={self.id!r}, name={self.name!r}, email1={self.email1!r})"


class LocationTable(ProjectBase):
    __tablename__ = 'locations'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_notion: Mapped[Optional[str]] = mapped_column(String(36))
    name: Mapped[str] = mapped_column(String(30))
    city: Mapped[str] = mapped_column(String(30))
    address: Mapped[Optional[str]] = mapped_column(String())
    purpose: Mapped[Optional[str]] = mapped_column(String())

    def __repr__(self) -> str:
        return f"LocationTable(id={self.id!r}, name={self.name!r}, city={self.city!r})"


class MusicTable(ProjectBase):
    __tablename__ = 'music'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_notion: Mapped[Optional[str]] = mapped_column(String(36))
    name: Mapped[str] = mapped_column(String(30))
    composer: Mapped[str] = mapped_column(String(30))
    voices: Mapped[Optional[str]] = mapped_column(String(20))
    instruments: Mapped[Optional[str]] = mapped_column(String(20))
    solo: Mapped[Optional[str]] = mapped_column(String(20))
    # TODO convert length from float to duration
    length: Mapped[Optional[float]] = mapped_column(Float(2))
    score: Mapped[Optional[str]] = mapped_column(String())
    media: Mapped[Optional[str]] = mapped_column(String())
    recording: Mapped[Optional[str]] = mapped_column(String())

    def __repr__(self) -> str:
        return f"MusicTable(id={self.id!r}, name={self.name!r}, composer={self.composer!r})"


class MusicProjectTable(ProjectBase):
    __tablename__ = 'music_project'

    id: Mapped[int] = mapped_column(primary_key=True)
    choir_id: Mapped[Optional[int]] = mapped_column(ForeignKey("choir.id"))
    id_notion: Mapped[Optional[str]] = mapped_column(String(36))
    name: Mapped[str] = mapped_column(String(30))
    year: Mapped[int] = mapped_column(Integer())
    status: Mapped[Optional[str]] = mapped_column(String(30))
    excerpt: Mapped[Optional[str]] = mapped_column(String())
    description: Mapped[Optional[str]] = mapped_column(String())

    choir = relationship("ChoirTable", foreign_keys=[choir_id])

    def __repr__(self) -> str:
        return f"MusicProjectTable(id={self.id!r}, name={self.name!r}, year={self.year!r}, choir_id={self.choir_id!r})"


class PartAllocationTable(ProjectBase):
    __tablename__ = 'part_allocation'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_notion: Mapped[Optional[str]] = mapped_column(String(36))
    name: Mapped[str] = mapped_column(String(30))
    music_id: Mapped[int] = mapped_column(
        ForeignKey("music.id"))
    music_project_id: Mapped[int] = mapped_column(
        ForeignKey("music_project.id"))
    staff_1: Mapped[Optional[str]] = mapped_column(String(36))
    staff_2: Mapped[Optional[str]] = mapped_column(String(36))
    staff_3: Mapped[Optional[str]] = mapped_column(String(36))
    staff_4: Mapped[Optional[str]] = mapped_column(String(36))
    staff_5: Mapped[Optional[str]] = mapped_column(String(36))
    staff_6: Mapped[Optional[str]] = mapped_column(String(36))
    staff_7: Mapped[Optional[str]] = mapped_column(String(36))
    staff_8: Mapped[Optional[str]] = mapped_column(String(36))
    staff_9: Mapped[Optional[str]] = mapped_column(String(36))
    staff_10: Mapped[Optional[str]] = mapped_column(String(36))
    staff_11: Mapped[Optional[str]] = mapped_column(String(36))
    staff_12: Mapped[Optional[str]] = mapped_column(String(36))
    notes: Mapped[Optional[str]] = mapped_column(String())
    selected: Mapped[bool] = mapped_column(Boolean())

    music_project = relationship(
        "MusicProjectTable", foreign_keys=[music_project_id])
    music = relationship("MusicTable", foreign_keys=[music_id])

    def __repr__(self) -> str:
        return f"PartAllocationTable(id={self.id!r}, name={self.name!r}, music_id={self.music_id!r}, music_project_id={self.music_project_id!r}, staff_1={self.staff_1!r})"


class RoleTable(ProjectBase):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    id_notion: Mapped[Optional[str]] = mapped_column(String(36))
    music_project_id: Mapped[int] = mapped_column(
        ForeignKey("music_project.id"))
    contact_id: Mapped[int] = mapped_column(ForeignKey("contacts.id"))
    note: Mapped[Optional[str]] = mapped_column(String())
    status: Mapped[Optional[str]] = mapped_column(String())

    music_project = relationship(
        "MusicProjectTable", foreign_keys=[music_project_id])
    contact = relationship("ContactTable", foreign_keys=[contact_id])

    def __repr__(self) -> str:
        return f"RoleTable(id={self.id!r}, name={self.name!r}, music_project_id={self.music_project_id!r}, contact_id={self.contact_id!r}, status={self.status!r})"


class TaskTable(ProjectBase):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_notion: Mapped[Optional[str]] = mapped_column(String(36))
    name: Mapped[Optional[str]] = mapped_column(String(30))
    start_date_time: Mapped[datetime] = mapped_column(DateTime())
    end_date_time: Mapped[Optional[datetime]] = mapped_column(DateTime())
    type: Mapped[Optional[str]] = mapped_column(String(15))
    music_project_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("music_project.id"))
    location_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("locations.id"))

    music_project = relationship(
        "MusicProjectTable", foreign_keys=[music_project_id])
    location = relationship(
        "LocationTable", foreign_keys=[location_id])

    def __repr__(self) -> str:
        return f"TaskTable(id={self.id!r}, name={self.name!r}, start_date_time={self.start_date_time!r}, end_date_time={self.end_date_time!r}, type={self.type!r}, music_project_id={self.music_project_id!r})"

class UserProjectRole(ProjectBase):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    project_id: Mapped[int] = mapped_column(ForeignKey('music_project.id'))
    role: Mapped[str] = mapped_column(
        Enum(UserProjectRoleEnum, native_enum=False, create_constraint=True), nullable=False)

    project = relationship("MusicProjectTable", foreign_keys=[project_id])