from datetime import date
from reduce_to_22 import reduce_to_22
from calculate_matrix import calculate_destiny_matrix
from family_fatal_error import calculate_family_errors, calculate_fatal_error


def calculate_soul_code(birth_date: date) -> dict:
    # Шаг 1: Рассчитываем матрицу судьбы
    user_data = calculate_destiny_matrix(birth_date)

    # Шаг 2: Рассчитываем родовые ошибки
    family_errors = calculate_family_errors(user_data)

    # Шаг 3: Рассчитываем роковую ошибку
    fatal_error = calculate_fatal_error(user_data)

    # Шаг 4: Получаем числа для кода души
    # Первое число — высшая миссия (из матрицы судьбы)
    first_number = user_data["soul_mission"]

    # Второе число — аркан, полученный при сложении родовых ошибок и роковой ошибки
    second_number = reduce_to_22(family_errors["father_error_male"] + family_errors["mother_error_male"] +
                                 family_errors["father_error_female"] + family_errors["mother_error_female"] +
                                 fatal_error["fatal_error"])

    # Третье число — аркан, полученный при сложении первого и второго числа
    third_number = reduce_to_22(first_number + second_number)

    return {
        "first_number": first_number,  # Миссия души (высшее предназначение)
        "second_number": second_number,  # Способ достижения
        "third_number": third_number,  # К чему в итоге приходит человек
    }


# Пример вызова для даты рождения:
test_date = date(1986, 11, 27)
soul_code = calculate_soul_code(test_date)
print(soul_code)
