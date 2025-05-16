from sqlalchemy import String, Integer, Date, ForeignKey, Enum as SqlEnum, JSON
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
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    personality: Mapped[int] = mapped_column(Integer, nullable=False)
    spirituality: Mapped[int] = mapped_column(Integer, nullable=False)
    money: Mapped[int] = mapped_column(Integer, nullable=False)
    relations: Mapped[int] = mapped_column(Integer, nullable=False)
    health: Mapped[int] = mapped_column(Integer, nullable=False)
    soul_mission: Mapped[int] = mapped_column(Integer, nullable=False)

    user: Mapped["Users"] = relationship(back_populates="user_data")


class ErrorType(PyEnum):
    karma = 'karma'
    family = 'family'
    major_past_error = 'major_past_error'


class UserErrors(Base):
    __tablename__ = 'user_errors'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    errors: Mapped[dict] = mapped_column(JSON)
    error_type: Mapped[ErrorType] = mapped_column(SqlEnum(ErrorType), nullable=False)

    user: Mapped["Users"] = relationship(back_populates="user_errors")