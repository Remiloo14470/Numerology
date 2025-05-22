from fastapi import HTTPException
from services.destiny_potential_matrix import calculate
from services.family_fatal_error import calculate_err
from services.soul_code import calс_soul_code
from app.models import requests
from app.models import responses
from database.initial import db
from uuid import uuid4
import base64
from app.api.initial import api_router
from fastapi.responses import JSONResponse
from database.models import Users, UserData, UserErrors, UserCodes
from utils.assistant_request import send_message_to_assistant
# from utils.generate_voice import synth_request_eleven_labs

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


@api_router.post("/demo-analysis/{user_id}", response_model=responses.DemoAnalysisResponse)
async def demo_analysis(data: requests.DemoAnalysisRequest):

    userdata = await db.get_row(UserData, user_id=data.user_id)
    if not userdata:
        raise HTTPException(status_code=204, detail="UserData not found")

    # Получаем family ошибки
    family_errors = await db.get_row(
        UserErrors,
        user_id=userdata.user_id,
        error_type="family",
    )
    if not family_errors:
        raise HTTPException(status_code=204, detail="Family errors not found")

    # Получаем karma ошибки
    karma_errors = await db.get_row(
        UserErrors,
        user_id=userdata.user_id,
        error_type="karma",
    )
    if not karma_errors:
        raise HTTPException(status_code=204, detail="Karma errors not found")

    # Извлекаем значения из JSON-полей
    try:
        errors_family = family_errors.errors
        errors_karma = karma_errors.errors

    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Missing key in error data: {e}")

    # Формируем промпт для ассистента
    prompt = (
        "Сделай краткий демо-анализ по духовному треугольнику пользователя на основе следующих данных:\n\n"
        f"- Основной показатель - аркан духовности: {userdata.spirituality}\n"
        "- Ошибки рода по духовной линии:\n"
        f"  • Левый канал (по женской линии): {errors_family['family_error_of_spirituality_left']}\n"
        f"  • Правый канал (по мужской линии): {errors_family['family_error_of_spirituality_right']}\n"
        f"  • Ошибки из прошлых воплощений: {errors_family['error_from_past_of_spirituality']}\n"
        "- Кармические ошибки:\n"
        f"  • Отца по мужской линии: {errors_karma['father_error_male']}\n"
        f"  • Матери по мужской линии: {errors_karma['mother_error_male']}\n\n"
        "Проанализируй эти цифры как нумеролог Надо Амири, кратко опиши сильные и слабые стороны, "
        "укажи, что может мешать духовному развитию, и как это может проявляться в жизни. "
        "Ответ должен быть кратким и понятным для обычного человека, как будто это первая встреча с нумерологией."
        "Тебе нужно описать эти цифры и покзать, что они взаимосвязаны с остальными цифрами его звезды. Заинтересовать"
        "клиента дальше раскрыть другие треугольники"
    )

    # Отправляем промпт с цифрами ассистенту
    response = await send_message_to_assistant(prompt)
    if not response:
        raise HTTPException(status_code=500, detail="Assistant failed to respond")

    # # Озвучиваем текст
    # audio_bytes = await synth_request_eleven_labs(text=response)
    # audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

    # Возвращаем результат
    return {
        "text": response
    }


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
async def calculate_soul_code(data: requests.SoulCodeRequest):
    user = await db.get_row(Users, id=data.user_id)
    if not user:
        raise HTTPException(status_code=204, detail="User not found")
    userdata = await db.get_row(UserData, user_id=data.user_id)
    if not userdata:
        raise HTTPException(status_code=204, detail="Content not found")

    soul_code = calс_soul_code(userdata)

    await db.add_row(
        UserCodes,
        user_id=user.id,
        numbers=soul_code,
        code_type='soul_code'
    )

    return JSONResponse(content={"soul_code": soul_code}, status_code=200)
