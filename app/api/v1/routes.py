from app.models.requests import *
from app.models.responses import *
from database.initial import db
from app.initial import api_router
from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response
from uuid import uuid4, UUID


# Эндпоинты

@api_router.post("/create-user", response_model= UserResponse, status_code=201)
async def create_user(user: UserRequest):
    new_row = await db.add_row(Users, user_id=user_id, user_name=user_name, date_of_birth=date_of_birth)
    result = await db.get_row(Users, id=new_row.id)
    response = {"data": result.get_data()}
    return JSONResponse(content=response, status_code=201)


@api_router.post("/demo-analysis")
async def demo_analysis(request: DemoAnalysisRequest):
    return JSONResponse(content={"message": f"Демо-анализ для даты рождения {data.birth_date}"}, status_code=200)


@api_router.post("/luck-code")
async def generate_luck_code(request: LuckCodeRequest):
    return JSONResponse(content={"luck_code": "12345"}, status_code=200)


@api_router.post("/generate-card")
async def generate_card(request: CardRequest):
    if request.card_type == "destiny":
        return JSONResponse(content={"message": "Рассчитываем Карту Судьбы"}, status_code=200)
    elif request.card_type == "time":
        return JSONResponse(content={"message": "Рассчитываем Карту Времени"}, status_code=200)


@api_router.post("/matrix")
async def calculate_matrix(request: MatrixRequest):
    return JSONResponse(content={
        "date_of_birth": request.date_of_birth,
        "matrix_type": request.matrix_type
    }, status_code=200)


@api_router.post("/compatibility")
async def check_compatibility(request: CompatibilityRequest):
    return JSONResponse(content={"compatibility_score": 85.0}, status_code=200)


@api_router.post("/family-error")
async def calculate_family_error(request: ErrorsRequest):
    if request.error_type == "carma":
        return JSONResponse(content={"message": "Рассчитываем Кармическую Ошибку"}, status_code=200)
    elif request.error_type == "family":
        return JSONResponse(content={"message": "Рассчитываем Ошибку Рода"}, status_code=200)


@api_router.post("/soul-mission")
async def calculate_soul_mission(request: SoulMissionRequest):
    return JSONResponse(content={"mission_info": "Информация о миссии души"}, status_code=200)


@api_router.post("/soul-code")
async def calculate_soul_code(request: SoulCodeRequest):
    return JSONResponse(content={"soul_code": "45678"}, status_code=200)
