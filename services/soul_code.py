from services.reduce_to_22 import reduce_to_22
from services.family_fatal_error import calculate_karma_errors


def calс_soul_code(userdata) -> dict:

    karma_errors = calculate_karma_errors(userdata)

    # Первое число — высшая миссия (из матрицы судьбы)
    first_number = userdata.soul_mission

    # Второе число — аркан, полученный при сложении родовых ошибок и роковой ошибки
    second_number = reduce_to_22(karma_errors["father_error_male"] + karma_errors["mother_error_male"] +
                                 karma_errors["father_error_female"] + karma_errors["mother_error_female"] +
                                 karma_errors["fatal_error"])

    # Третье число — аркан, полученный при сложении первого и второго числа
    third_number = reduce_to_22(first_number + second_number)

    return {
        "first_number": first_number,  # Миссия души (высшее предназначение)
        "second_number": second_number,  # Способ достижения
        "third_number": third_number,  # К чему в итоге приходит человек
    }
