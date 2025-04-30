from pydantic import BaseModel, Field, field_validator, model_validator
from enum import Enum
from typing import Optional


# Модели
class UserRequest(BaseModel):
    id: str = Field(alias='id')


class DemoAnalysisRequest(BaseModel):
    birth_of_date: str = Field(alias='birth')


class LuckCodeRequest(BaseModel):
    birth_of_date: str = Field(alias='birth')


class CardType(str, Enum):
    destiny = 'destiny'
    time = 'time'


class CardRequest(BaseModel):
    birth_of_date: str = Field(alias='birth')
    card_type: CardType


class MatrixType(str, Enum):
    potencial = 'potencial'
    destiny = 'destiny'


class MatrixRequest(BaseModel):
    birth_of_date: str = Field(alias='birth')
    matrix_type: MatrixType


class CompatibilityRequest(BaseModel):
    city: str = Field(alias='city')
    business: str = Field(alias='business')


class ErrorType(str, Enum):
    сarma_error = 'сarma'
    family_error = 'family'


class ErrorsRequest(BaseModel):
    user_id: str = Field(alias='user_id')
    error_type: ErrorType


class SoulMissionRequest(BaseModel):
    birth_of_date: str = Field(alias='birth')


class SoulCodeRequest(BaseModel):
    birth_of_date: str = Field(alias='birth')





