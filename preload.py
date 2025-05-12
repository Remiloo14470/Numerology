from app.api.initial import app, api_router
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.initial import db

from app.api.v1.routes import create_user, demo_analysis, generate_luck_code, generate_card, check_compatibility
from app.api.v1.routes import calculate_soul_code, calculate_soul_mission, calculate_matrix, calculate_family_error

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.initial()
    yield

root_app = FastAPI(lifespan=lifespan)

root_app.mount("/api/v1", app)
app.include_router(api_router, tags=['Routes'])

