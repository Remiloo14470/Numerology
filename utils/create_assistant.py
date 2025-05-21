from utils.get_async_client import client
from misc.assistant_info import assistant_info
from loguru import logger

# Создание ассистента
async def create_assistant():
    try:
        assistant = await client.beta.assistants.create(
            name="Numerology assistant",
            instructions=assistant_info,
            tools=[{"type": "file_search"}],
            model="gpt-4o",
        )
        logger.info(f"Ассистент создан: {assistant.id}")
        return assistant.id
    except Exception as e:
        logger.error(f"Ошибка при создании ассистента: {e}")
        return None