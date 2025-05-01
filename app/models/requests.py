from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional


# Модели
class UserRequest(BaseModel):
    id: str = Field(alias='id')
    user_name: str = Field(alias='user_name')
    date_of_birth: str = Field(alias='date_of_birth')


class DemoAnalysisRequest(BaseModel):
    date_of_birth: str = Field(alias='birth')


class LuckCodeRequest(BaseModel):
    date_of_birth: str = Field(alias='birth')


class CardType(str, Enum):
    destiny: str = Field(alias='destiny')
    time: str = Field(alias='time')


class CardRequest(BaseModel):
    date_of_birth: str = Field(alias='birth')
    card_type: CardType


class MatrixType(str, Enum):
    potencial: str = Field(alias='potencial')
    destiny = str = Field(alias='destiny')


class MatrixRequest(BaseModel):
    date_of_birth: str = Field(alias='birth')
    matrix_type: MatrixType


class CompatibilityRequest(BaseModel):
    city: str = Field(alias='city')
    business: str = Field(alias='business')


class ErrorType(str, Enum):
    сarma_error: str = Field(alias='сarma')
    family_error: str = Field(alias='family')


class ErrorsRequest(BaseModel):
    user_id: str = Field(alias='user_id')
    error_type: ErrorType


class SoulMissionRequest(BaseModel):
    date_of_birth: str = Field(alias='birth')


class SoulCodeRequest(BaseModel):
    date_of_birth: str = Field(alias='birth')





