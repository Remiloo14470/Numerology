from openai import AsyncOpenAI
from settings.project_settings import OtherSettings

settings = OtherSettings()

client = AsyncOpenAI(api_key=settings.openai_api_key)

