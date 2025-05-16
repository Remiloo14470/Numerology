from fastapi import HTTPException
from services.destiny_potential_matrix import calculate
from services.family_fatal_error import calculate_err
from app.models import requests
from app.models import responses
from database.initial import db
from uuid import uuid4
from app.api.initial import api_router
from fastapi.responses import JSONResponse
from database.models import Users, UserData, UserErrors

# Эндпоинты

@api_router.post("/create-user", response_model=responses.UserResponse)
async def create_user(data: requests.UserRequest):
    user_id = str(uuid4())
    existing_user, created = await db.get_or_create_row(
        Users,
        filter_by={"id": user_id},
        id=user_id,
        user_name=data.user_name,
        date_of_birth=data.date_of_birth,
    )
    return JSONResponse(
        content=responses.UserResponse.model_validate(existing_user).model_dump(),
        status_code=201 if created else 200
    )


@api_router.post("/demo-analysis")
async def demo_analysis(data: requests.DemoAnalysisRequest):

    return JSONResponse(content={"message": f"Демо-анализ для даты рождения {data.birth_date}"}, status_code=200)


@api_router.post("/luck-code")
async def generate_luck_code(data: requests.LuckCodeRequest):
    return JSONResponse(content={"luck_code": "12345"}, status_code=200)


@api_router.post("/generate-card")
async def generate_card(data: requests.CardRequest):
    if data.card_type == "destiny":
        return JSONResponse(content={"message": "Рассчитываем Карту Судьбы"}, status_code=200)
    elif data.card_type == "time":
        return JSONResponse(content={"message": "Рассчитываем Карту Времени"}, status_code=200)


@api_router.post("/matrix", response_model=responses.MatrixResponse)
async def calculate_matrix(data: requests.MatrixRequest):

    user = await db.get_row(Users, id=data.user_id)
    if not user:
        raise HTTPException(status_code=204, detail="User not found")

    matrix_data = calculate(user.date_of_birth, data.matrix_type)

    if data.matrix_type == requests.MatrixType.destiny:
        await db.add_row(
            UserData,
            user_id=user.id,
            **matrix_data
        )

    return JSONResponse(content={"matrix_data": matrix_data}, status_code=200)


@api_router.post("/compatibility")
async def check_compatibility(request: requests.CompatibilityRequest):
    return JSONResponse(content={"compatibility_score": 85.0}, status_code=200)


@api_router.post("/family-error", response_model=responses.ErrorResponse)
async def calculate_errors(data: requests.ErrorsRequest):
    user = await db.get_row(Users, id=data.user_id)
    if not user:
        raise HTTPException(status_code=204, detail="User not found")

    userdata = await db.get_row(UserData, user_id=data.user_id)
    if not userdata:
        raise HTTPException(status_code=204, detail="Content not found")

    if data.error_type == requests.ErrorType.karma:
        karma_errors = calculate_err("karma", userdata)
        await db.add_row(
            UserErrors,
            user_id=user.id,
            errors=karma_errors,
            error_type=data.error_type
        )


        return JSONResponse(content={"karma_errors": karma_errors}, status_code=200)

    elif data.error_type == requests.ErrorType.family:
        family_errors = calculate_err("family", userdata)
        await db.add_row(
            UserErrors,
            user_id=user.id,
            errors=family_errors,
            error_type=data.error_type
        )
        return JSONResponse(content={"family_errors": family_errors}, status_code=200)

@api_router.post("/soul-mission")
async def calculate_soul_mission(request: requests.SoulMissionRequest):
    return JSONResponse(content={"mission_info": "Информация о миссии души"}, status_code=200)


@api_router.post("/soul-code")
async def calculate_soul_code(request: requests.SoulCodeRequest):
    return JSONResponse(content={"soul_code": "45678"}, status_code=200)
