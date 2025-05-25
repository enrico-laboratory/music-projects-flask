from sqlalchemy import String, Enum, Integer, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)

from models.enums import UserRoleEnum

class AuthBase(DeclarativeBase):
    pass


class UserTable(AuthBase):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(), nullable=False)
    role: Mapped[str] = mapped_column(
        Enum(UserRoleEnum, native_enum=False, create_constraint=True), nullable=False)

