import asyncio

import uvicorn
from preload import *
# from utils.create_assistant import create_assistant
from app.api.v1.routes import create_user, demo_analysis, generate_luck_code, generate_card, check_compatibility
from app.api.v1.routes import calculate_soul_code, calculate_soul_mission, calculate_matrix, calculate_family_error

# async def startup() -> None:
#     assistant_id = create_assistant()
#     print(assistant_id)

if __name__ == "__main__":
    # asyncio.run(startup())
    uvicorn.run(app=root_app, host='127.0.0.1', port=5000)