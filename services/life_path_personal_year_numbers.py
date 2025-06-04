from datetime import date, datetime
from services.reduce_to_22 import reduce_to_22


def calculate_life_path_number(birth_date: date):
    date_to_digits = [int(ch) for ch in birth_date.strftime("%Y%m%d")]
    life_path_number = sum(date_to_digits)
    return reduce_to_22(life_path_number)


def calculate_personal_year(birth_date: date) -> int:
    current_year_sum = sum(int(ch) for ch in str(datetime.now().year))
    day_month_sum = sum(int(ch) for ch in birth_date.strftime("%m%d"))
    total = current_year_sum + day_month_sum
    return reduce_to_22(total)

