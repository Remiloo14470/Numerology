from sqlalchemy import String, Integer, Float, Date, ForeignKey
from database.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Users(Base):

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_name: Mapped[str] = mapped_column(String)
    date_of_birth: Mapped[str] = mapped_column(String)

class DestinyMatrix(Base):

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    personality: Mapped[int] = mapped_column(Integer)
    spirituality: Mapped[int] = mapped_column(Integer)
    money: Mapped[int] = mapped_column(Integer)
    relationship[int] = mapped_column(Integer)
    health[int] = mapped_column(Integer)