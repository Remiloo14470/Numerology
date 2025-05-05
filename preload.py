from app.api.initial import app, api_router
from fastapi import FastAPI

from app.api.v1.routes import create_user, demo_analysis, generate_luck_code, generate_card, check_compatibility
from app.api.v1.routes import calculate_soul_code, calculate_soul_mission, calculate_matrix, calculate_family_error

root_app = FastAPI(docs_url="/docs")

root_app.mount("/api/v1", app)
app.include_router(api_router, prefix="/api/v1", tags=['Routes'])

