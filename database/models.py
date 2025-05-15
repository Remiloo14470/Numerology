from sqlalchemy import String, Integer, Date, ForeignKey, Enum as SqlEnum
from database.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_name: Mapped[str] = mapped_column(String)
    date_of_birth: Mapped[Date] = mapped_column(Date)

    user_data: Mapped[list["UserData"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    user_errors: Mapped[list["UserErrors"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class UserData(Base):
    __tablename__ = 'user_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))

    personality: Mapped[int] = mapped_column(Integer)
    spirituality: Mapped[int] = mapped_column(Integer)
    money: Mapped[int] = mapped_column(Integer)
    relations: Mapped[int] = mapped_column(Integer)
    health: Mapped[int] = mapped_column(Integer)
    soul_mission: Mapped[int] = mapped_column(Integer)

    user: Mapped["Users"] = relationship(back_populates="user_data")


class ErrorType(PyEnum):
    karma = 'karma'
    family = 'family'


class UserErrors(Base):
    __tablename__ = 'user_errors'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))

    father_error_male: Mapped[int] = mapped_column(Integer)
    mother_error_male: Mapped[int] = mapped_column(Integer)
    father_error_female: Mapped[int] = mapped_column(Integer)
    mother_error_female: Mapped[int] = mapped_column(Integer)
    fatal_error: Mapped[int] = mapped_column(Integer)
    family_error_of_personality_left: Mapped[int] = mapped_column(Integer)
    family_error_of_personality_right: Mapped[int] = mapped_column(Integer)
    family_error_of_spirituality_left: Mapped[int] = mapped_column(Integer)
    family_error_of_spirituality_right: Mapped[int] = mapped_column(Integer)
    family_error_of_money_left: Mapped[int] = mapped_column(Integer)
    family_error_of_money_right: Mapped[int] = mapped_column(Integer)
    family_error_of_relations_left: Mapped[int] = mapped_column(Integer)
    family_error_of_relations_right: Mapped[int] = mapped_column(Integer)
    family_error_of_health_left: Mapped[int] = mapped_column(Integer)
    family_error_of_health_right: Mapped[int] = mapped_column(Integer)

    error_type: Mapped[ErrorType] = mapped_column(SqlEnum(ErrorType), nullable=False)
    user: Mapped["Users"] = relationship(back_populates="user_errors")