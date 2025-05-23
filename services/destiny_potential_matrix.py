from datetime import date
from services.reduce_to_22 import reduce_to_22


def calculate(birth_date: date, matrix_type: str) -> dict:
    if matrix_type == "destiny":
        return calculate_destiny_matrix(birth_date)
    elif matrix_type == "potential":
        pass
    else:
        raise ValueError("Invalid matrix type")


def calculate_destiny_matrix(birth_date: date) -> dict:
    day = reduce_to_22(birth_date.day)
    month = birth_date.month
    year = reduce_to_22(sum(int(d) for d in str(birth_date.year)))

    personality = day # Аркан дня рождения (верхний левый угол)
    spirituality = month # Аркан месяца рождения (верх центр угол)
    money = year # Аркан года рождения (верхн прав угол)
    relations = reduce_to_22(personality + spirituality + money) # Нижн прав угол
    health = reduce_to_22(personality + spirituality + money + relations) # Нижн лев угол
    """
        Миссия души это высшая миссия человека в этой жизни
    """
    soul_mission = reduce_to_22(personality + spirituality + money + relations + health) # центр звезды

    return {
        "personality": personality,
        "spirituality": spirituality,
        "money": money,
        "relations": relations,
        "health": health,
        "soul_mission": soul_mission
    }
