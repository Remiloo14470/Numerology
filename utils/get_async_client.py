from openai import AsyncOpenAI
from settings.project_settings import Settings

settings = Settings()

OPENAI_API_KEY = settings.openai_api_key

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

