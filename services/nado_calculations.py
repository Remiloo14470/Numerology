from datetime import date
from services.reduce_to_22 import reduce_to_22
import matplotlib.pyplot as plt


def reduce_to_9(n: int) -> int:
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


def energy_chart(birth_date: date, start_age: int = 17) -> dict:

    day_month = int(birth_date.strftime("%d%m"))
    energy_number = day_month * birth_date.year
    energy_str = str(energy_number)

    ages = list(range(start_age, start_age + len(energy_str)))
    energy_levels = [int(digit) for digit in energy_str]

    # Построение графика
    plt.figure(figsize=(12, 6))
    plt.plot(ages, energy_levels, marker='o', linestyle='-', color='purple')
    plt.title('График Жизненной Энергии')
    plt.xlabel('Возраст')
    plt.ylabel('Уровень энергии')
    plt.ylim(0, 9)
    plt.grid(True)
    plt.xticks(ages)
    plt.show()

    return {
        "birth_date": birth_date.isoformat(),
        "energy_number": energy_number,
        "energy_levels": energy_levels,
        "ages": ages,
    }


def financial_forecast(energy_levels: list[int], ages: list[int]) -> dict:
    """
    Возвращает словарь с финансовыми пиками жизненной энергии:
    годы, в которых уровень энергии 8 или 9.
    """
    financial_peaks = [
        {"age": age, "level": level}
        for age, level in zip(ages, energy_levels)
        if level in (8, 9)
    ]

    return {
        "financial_peaks": financial_peaks,
        "count": len(financial_peaks),
        "strong_years": [peak["age"] for peak in financial_peaks]
    }


def calculate_luck_number_by_weekday(birth_date: date) -> int:
    """
    Число удачи по дню недели
    Преобразует день недели в соотв. число удачи.
    """
    day_codes = {
        0: 2,  # пн
        1: 9,  # вт
        2: 5,  # ср
        3: 3,  # чт
        4: 6,  # пт
        5: 7,  # суб
        6: 1,  # вс
    }
    weekday = birth_date.weekday()  # 0 - понедельник, ..., 6 - воскресенье
    code = day_codes.get(weekday)
    luck_number = code + 1
    return luck_number


def calculate_protection_number(birth_date: date) -> int:
    """
    Число защиты
    Сумма дня и месяца рождения, приведённая к диапазону 1–22.
    """
    protection_number = reduce_to_22(sum(int(ch) for ch in birth_date.strftime("%d%m")))
    return protection_number


def calculate_mirror_protection(personal_year_number: int, life_path_number: int) -> int:
    """
    Вычисляет Зеркальную защиту как сумму Персонального года и Числа судьбы,
    сведенные к от 1 до 22.
    """
    total = personal_year_number + life_path_number
    mirror_protection = reduce_to_22(total)
    return mirror_protection


def calculate_life_map(personal_year_number: int) -> dict:
    """
    Расчёт life_map (карты судьбы) на год.
    Возвращает словарь с месяцами и арканами месяцев.

    """

    life_map = {}
    for month in range(1, 13):
        arcana = reduce_to_22(personal_year_number + month)
        life_map[month] = arcana
    return life_map


def calculate_time_code(life_path_number: int, personal_year_number: int) -> int:
    time_code = reduce_to_22(life_path_number+personal_year_number)
    return time_code


def calculate_city_country_code(birth_date: date, life_path_number: int, city_name: str) -> dict:
    mapping = {
        'А': 1, 'И': 1, 'С': 1, 'Ъ': 1,
        'Б': 2, 'Й': 2, 'Т': 2, 'Ы': 2,
        'В': 3, 'К': 3, 'У': 3, 'Ь': 3,
        'Г': 4, 'Л': 4, 'Ф': 4, 'Э': 4,
        'Д': 5, 'М': 5, 'Х': 5, 'Ю': 5,
        'Е': 6, 'Н': 6, 'Ц': 6, 'Я': 6,
        'Ё': 7, 'О': 7, 'Ч': 7,
        'Ж': 8, 'П': 8, 'Ш': 8,
        'З': 9, 'Р': 9, 'Щ': 9
    }
    city_number = 0

    for char in city_name.upper():
        if char in mapping:
            city_number += mapping[char]

    reduced_city_number = reduce_to_9(city_number)

    # Вычисляем совместимость со страной
    country_number = reduce_to_9(birth_date.day)
    life_path_number = reduce_to_9(life_path_number)

    if life_path_number in [11,22,33]:
        life_path_number = 2

    return {
        "city_number": reduced_city_number,
        "country_number": country_number,
        "life_path_number_for_country": life_path_number
    }


def calculate_business_compatibility(reg_date: date, life_path_number: int) -> int:
    business_number = reduce_to_9(sum(int(ch) for ch in reg_date.strftime("%Y%d%m")))
    return business_number



