from sqlalchemy import Column, String, Integer, Float, Date
from database.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Users(Base):
    id: Mapped[str] = mapped_column(String, primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(String)
    date_of_birth: Mapped[str] = mapped_column(String)
