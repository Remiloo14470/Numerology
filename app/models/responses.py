from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: str = Field(alias='id')

class DemoAnalysisResponse(BaseModel):
    message: str = Field(alias='message')

class LuckCodeResponse(BaseModel):
    luck_code: str = Field(alias='luck_code')

class CardTypeResponse(BaseModel):
    cardtype: str = Field(alias='cardtype')

class MatrixResponse(BaseModel):
    status: str = Field(alias='status')
    result: str = Field(alias='result')

class CompatibilityResponse(BaseModel):
    compatibility_score: float = Field(alias='compatibility_score')

class SoulMissionResponse(BaseModel):
    mission_info: str = Field(alias='mission_info')

class SoulCodeResponse(BaseModel):
    soul_code: str = Field(alias='soul_code')