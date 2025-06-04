from services.reduce_to_22 import reduce_to_22
from datetime import date

def calculate_luck_code(personal_year: int) -> dict:
    stability_code = reduce_to_22(personal_year + 4)
    prosperity_code = reduce_to_22(personal_year + 8)
    return {
        "stability_code": stability_code,
        "prosperity_code": prosperity_code,
    }


def calculate_luck_rhythm(personal_year: int, life_path_number: int) -> dict:
    luck_rhythm = reduce_to_22(personal_year + life_path_number)
    return {"luck_rhythm": luck_rhythm}


def calculate_luck_rhythm_by_birthday(birth_date: date) -> dict:
    luck_number_by_birthday = reduce_to_22(birth_date.day)
    """Возвращает дни месяца, сумма цифр которых даёт число удачи."""

    strong_days = [
        day for day in range(1, 32)
        if reduce_to_22(day) == luck_number_by_birthday
    ]
    return {
        "luck_number_by_birthday": luck_number_by_birthday,
        "strong_days": strong_days
    }


def calculate_luck_rhythm_by_month(birth_date: date) -> dict:
