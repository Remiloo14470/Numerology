import asyncio
from utils.get_async_client import client
from loguru import logger
from utils.assistant_state import assistant_id

async def send_message_to_assistant(prompt: str) -> str:
    thread = await client.beta.threads.create()
    logger.info(f"ID Ассистента {assistant_id}")
    message = await client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )

    run = await client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )
    # Ожидаем завершения работы ассистента
    for _ in range(30):
        await asyncio.sleep(2)
        run = await client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        if run.status == "completed":
            messages = await client.beta.threads.messages.list(thread_id=thread.id)
            return messages.data[0].content[0].text.value

        elif run.status not in ["queued", "in_progress"]:
            logger.warning(f"Ассистент завершился со статусом: {run.status}")
            raise RuntimeError(f"Ассистент не смог завершить работу. Статус: {run.status}")

    # Если цикл завершился без результата
    logger.warning("Время ожидания ответа от ассистента истекло")
    raise TimeoutError("Ассистент не ответил в течение 60 секунд")
