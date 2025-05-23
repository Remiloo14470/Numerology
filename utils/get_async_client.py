from openai import AsyncOpenAI
from settings.project_settings import APISettings

settings = APISettings()

client = AsyncOpenAI(api_key=settings.openai_api_key)

