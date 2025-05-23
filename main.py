import asyncio
import uvicorn
from preload import *


# async def startup():
#     await start_assistant()
#     print("Assistant ID:", assistant_state.assistant_id)

if __name__ == "__main__":
    # asyncio.run(startup())
    uvicorn.run(app=root_app, host='127.0.0.1', port=5000)