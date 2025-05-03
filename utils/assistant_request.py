import re
import json
import asyncio
import time
from loguru import logger
from openai import APIConnectionError, OpenAIError
from utils.create_assistant import assistant_id
from utils.get_async_client import client
from utils import assistant_prompt


async def send_message_to_assistant():
    try:
        prompt = assistant_prompt.format(str)

        thread = await client.beta.threads.create()
        logger.debug(f"Adding message to thread {thread.id}")
        thread_message = await client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt
        )

        run_assistant = await client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        start_time = time.time()
        timeout = 120

        while run_assistant.status in ["queued", "in_progress"]:
            if time.time() - start_time > timeout:
                logger.warning(f"Run time out for thread {thread.id}")

                return None

            keep_retrieving_run = await client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run_assistant.id
            )

            logger.debug(f"Run status: {keep_retrieving_run.status}")

            run_assistant = keep_retrieving_run

            if keep_retrieving_run.status == "completed":

                messages = await client.beta.threads.messages.list(thread_id=thread.id)
                answer = messages.data[0].content[0].text.value
                answer = re.sub(r"``json\n(.*?)\n``", r"\1", answer, flags=re.DOTALL)
                response_data = json.loads(answer)
                return response_data
            elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
                pass
            else:
                logger.warning(f"Couldn't to get response, status: {keep_retrieving_run.status}")
                return None
            await asyncio.sleep(4)

    except APIConnectionError as exc:
        logger.debug(f"Failed to connect to OpenAI API: {exc}")
        return None
    except OpenAIError as exc:
        logger.debug(f"OpenAI API error: {exc}")
        return None
    except Exception as exc:
        logger.debug(exc)