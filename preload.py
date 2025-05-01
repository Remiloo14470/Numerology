from app.api.initial import app, api_router
from fastapi import FastAPI
from utils.get_async_client import client
from utils import assistant_prompt
import logging

root_app = FastAPI()

root_app.mount("/api/v1", app)
app.include_router(api_router, tags=['routes'])

# Создание ассистента
async def create_assistant():
    try:
        assistant = await client.beta.assistants.create(
            name="Starlik sales assistant",
            instructions=assistant_prompt,
            model="gpt-4o",
        )
        logging.info(f"Ассистент создан: {assistant.id}")
        return assistant.id
    except Exception as e:
        logging.error(f"Ошибка при создании ассистента: {e}")
        return None
assistant_id = create_assistant()