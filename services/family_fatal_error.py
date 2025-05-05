from reduce_to_22 import reduce_to_22
from calculate_matrix import user_data

data = user_data


def calculate_family_errors(data):
    """Расчет ошибок рода."""

    father_error_male = reduce_to_22(data["personality"] + data["spirituality"])
    mother_error_male = reduce_to_22(data["spirituality"] + data["money"])
    father_error_female = reduce_to_22(data["money"] + data["relationship"])
    mother_error_female = reduce_to_22(data["health"] + data["personality"])
    fatal_error = reduce_to_22(data["relationship"] + data["health"])

    return {
        'father_error_male': father_error_male,
        'mother_error_male': mother_error_male,
        'father_error_female': father_error_female,
        'mother_error_female': mother_error_female,
    }

def calculate_fatal_error(data: dict):  # Роковая ошибка прошлой жизни
    relationships = data["relationship"]
    health = data["health"]
    fatal_error = reduce_to_22(relationships + health)
    return {'fatal_error': fatal_error}


if __name__ == "__main__":

    result = calculate_family_errors(data)
    result1 = calculate_fatal_error(data)
    print(result, result1)