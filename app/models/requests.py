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
    user_id: str


class RelationsRequest(BaseModel):
    user_id: str
    partner_birthdate: str = Field(..., pattern=r'^\d{2}-\d{2}-\d{4}$')  # строка ДД-ММ-ГГГГ

    @field_validator('partner_birthdate')
    def validate_date_of_birth(cls, v: str) -> date:
        try:
            return datetime.strptime(v, "%d-%m-%Y").date()
        except:
            raise HTTPException(status_code=400,
                                detail=f"Дата некорректна. Пожалуйста, проверьте правильность дня, месяца и года.")


class LuckCodeRequest(BaseModel):
    date_of_birth: date = Field(alias='birth')


class CompatibilityRequest(BaseModel):
    city: str = Field(alias='city')
    business: str = Field(alias='business')



class SoulMissionRequest(BaseModel):
    user_id: str


class SoulCodeRequest(BaseModel):
    user_id: str





