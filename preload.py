from fastapi import FastAPI
from app.initial import *

root_app = FastAPI(lifespan=lifespan)

root_app.mount("/api/v1", app)
app.include_router(api_router, tags=['routes'])
