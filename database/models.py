from sqlalchemy import String, Integer, Float, Date, ForeignKey
from database.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_name: Mapped[str] = mapped_column(String)
    date_of_birth: Mapped[str] = mapped_column(String)

class UserData(Base):
    __tablename__ = 'user_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    personality: Mapped[int] = mapped_column(Integer)
    spirituality: Mapped[int] = mapped_column(Integer)
    money: Mapped[int] = mapped_column(Integer)
    relationship: Mapped[int] = mapped_column(Integer)
    health: Mapped[int] = mapped_column(Integer)
    soul_mission: Mapped[int] = mapped_column(Integer)