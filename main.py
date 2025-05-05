import asyncio

import uvicorn
from preload import *
# from utils.create_assistant import create_assistant


# async def startup() -> None:
#     assistant_id = create_assistant()
#     print(assistant_id)

if __name__ == "__main__":
    # asyncio.run(startup())
    uvicorn.run(app=root_app, host='127.0.0.1', port=5000)