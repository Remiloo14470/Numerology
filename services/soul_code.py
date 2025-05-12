from reduce_to_22 import reduce_to_22
from destiny_potential_matrix import user_data
from family_fatal_error import calculate_karma_errors, calculate_fatal_error


def calculate_soul_code():

    global user_data
    data = user_data
    karma_errors = calculate_karma_errors()
    fatal_error = calculate_fatal_error()


    # Первое число — высшая миссия (из матрицы судьбы)
    first_number = data["soul_mission"]

    # Второе число — аркан, полученный при сложении родовых ошибок и роковой ошибки
    second_number = reduce_to_22(karma_errors["father_error_male"] + karma_errors["mother_error_male"] +
                                 karma_errors["father_error_female"] + karma_errors["mother_error_female"] +
                                 fatal_error["fatal_error"])

    # Третье число — аркан, полученный при сложении первого и второго числа
    third_number = reduce_to_22(first_number + second_number)

    return {
        "first_number": first_number,  # Миссия души (высшее предназначение)
        "second_number": second_number,  # Способ достижения
        "third_number": third_number,  # К чему в итоге приходит человек
    }

soul_code = calculate_soul_code()

if __name__ == '__main__':

    print(soul_code)
