from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator
from enum import Enum
from datetime import date, datetime


# Schemas

class UserRequest(BaseModel):
    id: str = Field(alias='id')
    user_name: str = Field(alias='user_name')
    date_of_birth: str = Field(..., pattern=r'^\d{2}-\d{2}-\d{4}$')  # строка ДД-ММ-ГГГГ


    @field_validator('date_of_birth')
    def validate_date_of_birth(cls, v: str) -> date:
        try:
            return datetime.strptime(v, "%d-%m-%Y").date()
        except:
            raise HTTPException(status_code=400, detail=f"Дата некорректна. Пожалуйста, проверьте правильность дня, месяца и года.")

class DemoAnalysisRequest(BaseModel):
    date_of_birth: str = Field(alias='birth')


class LuckCodeRequest(BaseModel):
    date_of_birth: date = Field(alias='birth')


class CardType(str, Enum):
    destiny ='destiny'
    time ='time'


class CardRequest(BaseModel):
    date_of_birth: date = Field(alias='birth')
    card_type: CardType


class MatrixType(str, Enum):
    potential = 'potential'
    destiny = 'destiny'


class MatrixRequest(BaseModel):
    user_id: str
    matrix_type: MatrixType


class CompatibilityRequest(BaseModel):
    city: str = Field(alias='city')
    business: str = Field(alias='business')


class ErrorType(str, Enum):
    karma = 'karma'
    family = 'family'


class ErrorsRequest(BaseModel):
    user_id: str
    error_type: ErrorType


class SoulMissionRequest(BaseModel):
    date_of_birth: str = Field(alias='birth')


class SoulCodeRequest(BaseModel):
    date_of_birth: date = Field(alias='birth')





