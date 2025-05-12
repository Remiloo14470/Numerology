from uuid import UUID

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    class Info(BaseModel):
        id: UUID
        user_name: str = Field(alias='user_name')
        date_of_birth: str = Field(alias='date_of_birth')
    class Error(BaseModel):
        error: str

    class Config:
        from_attributes = True


class DemoAnalysisResponse(BaseModel):
    class Info(BaseModel):
        message: str = Field(alias='message')
    class Error(BaseModel):
        error: str

class LuckCodeResponse(BaseModel):
    class Info(BaseModel):
        luck_code: str = Field(alias='luck_code')
    class Error(BaseModel):
        error: str

class CardTypeResponse(BaseModel):
    class Info(BaseModel):
        card_type: str = Field(alias='cardtype')
    class Error(BaseModel):
        error: str

class MatrixResponse(BaseModel):
    class Info(BaseModel):
        status: str = Field(alias='status')
        result: str = Field(alias='result')
    class Error(BaseModel):
        error: str

class CompatibilityResponse(BaseModel):
    class Info(BaseModel):
        compatibility_score: float = Field(alias='compatibility_score')
    class Error(BaseModel):
        error: str

class SoulMissionResponse(BaseModel):
    class Info(BaseModel):
        mission_info: str = Field(alias='mission_info')
    class Error(BaseModel):
        error: str

class SoulCodeResponse(BaseModel):
    class Info(BaseModel):
        soul_code: str = Field(alias='soul_code')
    class Error(BaseModel):
        error: str