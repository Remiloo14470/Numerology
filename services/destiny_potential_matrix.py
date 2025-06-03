from datetime import date
from services.reduce_to_22 import reduce_to_22


def calculate(birth_date: date, matrix_type: str) -> dict:
    if matrix_type == "destiny":
        return calculate_destiny_matrix(birth_date)
    elif matrix_type == "potential":
        return calculate_potential_matrix(birth_date)
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


def calculate_potential_matrix(birth_date: date) -> dict:

    # 1. Число Судьбы = сумма всех цифр даты рождения
    destiny_number = reduce_to_22(sum(int(d) for d in birth_date.strftime("%d%m%Y")))

    # 2. Число Потенциала = сумма дня и месяца рождения
    potential_number = reduce_to_22(sum(int(d) for d in birth_date.strftime("%d%m")))

    # 3. Число Реализации = Судьба + Потенциал
    realization_number = reduce_to_22(destiny_number + potential_number)

    # 4. Кармическое число = Судьба - Потенциал
    karma_number = reduce_to_22(abs(destiny_number - potential_number))

    # 5. Число Успеха = Реализация + Потенциал
    success_number = reduce_to_22(realization_number + potential_number)

    return {
        "destiny_number": destiny_number,
        "potential_number": potential_number,
        "realization_number": realization_number,
        "karma_number": karma_number,
        "success_number": success_number
    }