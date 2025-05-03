from app.api.initial import app, api_router
from fastapi import FastAPI

root_app = FastAPI(docs_url="/app/api/v1/docs")

root_app.mount("/api/v1", app)
app.include_router(api_router, prefix="/api/v1", tags=['routes'])

