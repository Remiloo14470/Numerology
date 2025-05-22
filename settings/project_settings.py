from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):

    db_host: str = Field(alias='dbhost')
    db_port: int = Field(alias='dbport')
    db_name: str = Field(alias='dbname')
    db_user: str = Field(alias='dbuser')
    db_password: str = Field(alias='dbpassword')
    openai_api_key: str = Field(alias="openai_api_key")
    # eleven_labs_api_key: str = Field(alias='eleven_labs_api_key')
    # eleven_labs_voice_id: str = Field(alias='eleven_labs_voice_id')

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

