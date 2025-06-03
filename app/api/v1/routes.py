from fastapi import HTTPException
from services.destiny_potential_matrix import calculate
from services.family_fatal_error import calculate_errors
from services.partner_numbers import calc_partners_numbers
from services.gen_luck_code_and_rhythm import calculate_luck_code, calculate_luck_rhythm
from services.soul_code import calculate_soul_code
from services.life_path_personal_year_numbers import calculate_personal_year, calculate_life_path_number
from app.models import requests
from app.models import responses
from database.initial import db
from uuid import uuid4
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
        user_name_surname=data.user_name_surname,
        date_of_birth=data.date_of_birth,
    )

    user = await db.get_row(Users, id=user_id)
    if not user:
        raise HTTPException(status_code=204, detail="User not found")

    matrix_data = calculate(user.date_of_birth, matrix_type="destiny")
    personal_year_number = calculate_personal_year(user.date_of_birth)
    destiny_number = calculate_life_path_number(user.date_of_birth)

    await db.add_row(
        UserData,
        user_id=user.id,
        personal_year_number=personal_year_number,
        destiny_number=destiny_number,
        **matrix_data
    )

    userdata = await db.get_row(UserData, user_id=user_id)
    if not userdata:
        raise HTTPException(status_code=204, detail="Content not found")

    karma_errors = calculate_errors("karma", userdata)
    await db.add_row(
        UserErrors,
        user_id=user.id,
        errors=karma_errors,
        error_type="karma"
    )

    family_errors = calculate_errors("family", userdata)
    await db.add_row(
        UserErrors,
        user_id=user.id,
        errors=family_errors,
        error_type="family"
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
        "Сделай краткий демо-анализ по духовному треугольнику пользователя на основе следующих данных:\n"
        f"- Основной показатель — аркан духовности: {userdata.spirituality}\n"
        "- Ошибки рода по духовной линии:\n"
        f"  • Левый канал (по женской линии): {errors_family['family_error_of_spirituality_left']}\n"
        f"  • Правый канал (по мужской линии): {errors_family['family_error_of_spirituality_right']}\n"
        f"  • Ошибки из прошлых воплощений: {errors_family['error_from_past_of_spirituality']}\n"
        "- Кармические ошибки:\n"
        f"  • Отца по мужской линии: {errors_karma['father_error_male']}\n"
        f"  • Матери по мужской линии: {errors_karma['mother_error_male']}\n\n"
        "Проанализируй эти цифры как нумеролог Надо Амири. Кратко опиши сильные и слабые стороны, "
        "укажи, что может мешать духовному развитию и как это может проявляться в жизни.\n"
        "Ответ должен быть понятным для обычного человека, как будто это первая встреча с нумерологией.\n"
        "Опиши эти цифры и покажи, что они взаимосвязаны с остальными цифрами его звезды. Заинтересуй "
        "клиента раскрыть другие треугольники."
    )

    # Отправляем промпт с цифрами ассистенту
    response = await send_message_to_assistant(prompt)
    if not response:
        raise HTTPException(status_code=500, detail="Assistant failed to respond")

    # # Озвучиваем текст
    # audio_bytes = await synth_request_eleven_labs(text=response)
    # audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

    return JSONResponse(content={"response": response}, status_code=200)

@api_router.post("/generate_luck_code_and_rhythm", response_model=responses.LuckCodeResponse)
async def generate_luck_code_and_rhythm(data: requests.LuckCodeRequest):
    # Получение персонального года из UserData
    userdata = await db.get_row(UserData, user_id=data.user_id)

    if not userdata or userdata.personal_year_number is None:
        raise HTTPException(status_code=404, detail="Personal year not found for user")

    luck_codes = calculate_luck_code(userdata.personal_year_number)
    luck_rhythm = calculate_luck_rhythm(userdata.personal_year_number, userdata.destiny_number)

    await db.add_row(
        UserCodes,
        user_id=data.user_id,
        numbers=luck_codes,
        code_type="luck_code"
    )

    prompt = (
        "Ты — профессиональный нумеролог и духовный наставник, который помогает людям видеть свою уникальную дорогу и принимать сильные решения."
        "Твоя задача — глубоко анализировать годовые тенденции человека. Ты создаёшь живую, осознанную стратегию на год.\n"
        "Твоя задача — по коду персонального года пользователя вычислить и интерпретировать два значения:\n"
        "- Код стабильности (Персональный год + 4)\n"
        "- Код процветания (Персональный год + 8)\n\n"

        f"Персональный год пользователя: {userdata.personal_year_number}\n"
        f"Код стабильности: {luck_codes['stability_code']}\n"
        f"Код процветания: {luck_codes['prosperity_code']}\n\n"

        "Интерпретируй значения этих кодов так, как если бы они соответствовали Арканам:\n"
        f"- Что даёт силу и устойчивость ({luck_codes['stability_code']})\n"
        f"- Через что приходит успех, деньги, возможности ({luck_codes['prosperity_code']})\n"
        "- Приведи конкретные жизненные сценарии и рекомендации\n"
        "- Используй честный, но мягкий, поддерживающий тон\n\n"

        "Поясни, как эти энергии могут повлиять на год, какие качества важно развивать, какие ошибки избегать, "
        "и какие выборы приведут к внутреннему и внешнему росту. Заверши вдохновляющим инсайтом — выводом, "
        "который пользователь может взять с собой как стратегию на год.\n\n"
        "Далее Нумерологический ритм удачи: календарная стратегия на год"
        
        f"Используй Число судьбы: {userdata.destiny_number}"
        f"Ритм удачи: {luck_rhythm}"
        "Используется для выявления сильных и слабых дней и месяцев."
        
        "Благоприятные дни: 3, 6, 9, 12, 15, 21, 30 → Назначай важные встречи, начинай дела, принимай решения.\n"
        "Неблагоприятные дни: 4, 8, 13, 17, 26 → Замедлись, не принимай решений в стрессе, не дави.\n"
        "Месяцы удачи:Март, Май, Август, Октябрь → Рост, проекты, раскрытие.\n"
        "Слабые месяцы: Февраль, Июнь, Сентябрь → Пауза, внутренняя работа, завершения.\n"
        
        "Расскажи человеку, как использовать этот ритм:"
        "Когда действовать, Когда отдыхать, Когда быть особенно внимательным. Сделай это как ежедневную стратегию, "
        "встроенную в ритмы года.\n"
        "Финальная структура ответа (всегда сохраняй стиль живого наставника):"
        f"Аркан года ({userdata.personal_year_number}) — его смысл, вызовы и путь."
        f"информацию по всем арканам бери из веркторного хранилища"
        "Код стабильности — как опираться и не потеряться."
        "Код процветания — как раскрыть рост, деньги, успех."
        "Нумерологический ритм года:"
        "Благоприятные и неблагоприятные дни"
        "Сильные и слабые месяцы"
        "Как встроиться в эти ритмы и выстроить год как стратегию.\n"
        "Пример подачи: "
        "Не просто “вот числа”, а:"
        "— “Что это даёт тебе?”"
        "— “Как это использовать в жизни?”"
        "— “В чём твоя точка силы и роста?”"
        "— “Что ты можешь сделать уже в этом месяце?”"
    )

    response = await send_message_to_assistant(prompt)
    if not response:
        raise HTTPException(status_code=500, detail="Assistant failed to respond")

    return JSONResponse(content={"response": response}, status_code=200)

#
# @api_router.post("/generate-card")
# async def generate_card(data: requests.CardRequest):
#     if data.card_type == "destiny":
#         return JSONResponse(content={"message": "Рассчитываем Карту Судьбы"}, status_code=200)
#     elif data.card_type == "time":
#         return JSONResponse(content={"message": "Рассчитываем Карту Времени"}, status_code=200)


@api_router.post("/relations", response_model=responses.RelationsResponse)
async def calculate_relations(data: requests.RelationsRequest):

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

    # расчитываем числа партнера
    # partners_numbers = calc_partners_numbers(data.partner_birthdate)
    #
    # # сохраняем в базу если еще нет
    # partner_row, created = await db.get_or_create_row(
    #     model=UserPartners,
    #     filter_by={"user_id": data.user_id, "partner_birthdate": data.partner_birthdate},
    #     user_id=data.user_id,
    #     partner_matrix=partners_numbers["partner_matrix"],
    #     partner_karma=partners_numbers["partner_karma"],
    #     partner_family=partners_numbers["partner_family"]
    # )
    #
    # # извлекаем из базы и используем в ассистенте
    # relations = partner_row.partner_matrix.get("relations")
    #
    # father_error_female = partner_row.partner_karma.get("father_error_female")
    # fatal_error = partner_row.partner_karma.get("fatal_error")
    #
    # family_error_left = partner_row.partner_family.get("family_error_of_relations_left")
    # family_error_right = partner_row.partner_family.get("family_error_of_relations_right")
    # error_from_past = partner_row.partner_family.get("error_from_past_of_relations")


    # Формируем промпт для ассистента
    prompt = (
        "Сделай глубокий анализ отношений пользователя на основе следующих данных из треугольника отношений:\n"
        f"- Основной показатель — аркан отношений: {userdata.relations}\n"
        "- Ошибки рода по линии отношений:\n"
        f"  • Левый канал (по женской линии): {errors_family['family_error_of_relations_left']}\n"
        f"  • Правый канал (по мужской линии): {errors_family['family_error_of_relations_right']}\n"
        f"  • Ошибки из прошлых воплощений: {errors_family['error_from_past_of_relations']}\n"
        "- Кармические ошибки:\n"
        f"  • Ошибка по отцу (женская энергия): {errors_karma['father_error_female']}\n"
        f"  • Фатальная ошибка: {errors_karma['fatal_error']}\n\n"
        "Проанализируй эти цифры как нумеролог Надо Амири. Раскрой:\n"
        "1. Подробный разбор сферы отношений пользователя.\n"
        "2. Значение каждой цифры и её влияние на личную жизнь.\n"
        "3. Как раскрыть энергию этих чисел для гармонизации отношений.\n"
        "4. Бонус: Опиши, какой партнёр подходит пользователю по энергиям и чему он может научиться в отношениях.\n\n"
        "Ответ должен быть понятным, как для новичка в нумерологии, цепляющим и вовлекающим. Сделай акцент на внутреннем росте, "
        "влиянии прошлого, и покажи, что эти данные — только начало более глубокого понимания себя."
    )

    # Отправляем промпт с цифрами ассистенту
    response = await send_message_to_assistant(prompt)
    if not response:
        raise HTTPException(status_code=500, detail="Assistant failed to respond")

    return JSONResponse(content={
        "response": response
    }, status_code=200)


@api_router.post("/compatibility")
async def check_compatibility(request: requests.CompatibilityRequest):
    return JSONResponse(content={"compatibility_score": 85.0}, status_code=200)


@api_router.post("/family-error")


@api_router.post("/soul-mission")
async def calculate_soul_mission(request: requests.SoulMissionRequest):
    return JSONResponse(content={"mission_info": "Информация о миссии души"}, status_code=200)


@api_router.post("/soul-code")
async def calc_soul_code(data: requests.SoulCodeRequest):
    user = await db.get_row(Users, id=data.user_id)
    if not user:
        raise HTTPException(status_code=204, detail="User not found")

    userdata = await db.get_row(UserData, user_id=data.user_id)
    if not userdata:
        raise HTTPException(status_code=204, detail="Content not found")

    soul_code = calculate_soul_code(userdata)

    await db.add_row(
        UserCodes,
        user_id=user.id,
        numbers=soul_code,
        code_type='soul_code'
    )

    return JSONResponse(content={"soul_code": soul_code}, status_code=200)
