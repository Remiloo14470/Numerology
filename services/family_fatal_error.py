from reduce_to_22 import reduce_to_22
from calculate_matrix import user_data

data = user_data


def calculate_karma_errors():
    """Расчет кармических ошибок."""

    father_error_male = reduce_to_22(data["personality"] + data["spirituality"])
    mother_error_male = reduce_to_22(data["spirituality"] + data["money"])
    father_error_female = reduce_to_22(data["money"] + data["relationship"])
    mother_error_female = reduce_to_22(data["health"] + data["personality"])

    return {
        'father_error_male': father_error_male,
        'mother_error_male': mother_error_male,
        'father_error_female': father_error_female,
        'mother_error_female': mother_error_female,
    }

karma_errors = calculate_karma_errors()


def calculate_fatal_error():  # Роковая ошибка прошлой жизни
    relationships = data["relationship"]
    health = data["health"]
    fatal_err = reduce_to_22(relationships + health)
    return {
        'fatal_error': fatal_err
    }

fatal_error = calculate_fatal_error()

def calculate_family_errors():
    """Расчет родовых ошибок - кармических уроков"""

    family_error_of_personality_left = reduce_to_22(karma_errors['mother_error_female'] + data['personality'])
    family_error_of_personality_right =reduce_to_22(karma_errors['father_error_male'] + data['personality'])
    family_error_of_spirituality_left =reduce_to_22(karma_errors['father_error_male'] + data['spirituality'])
    family_error_of_spirituality_right =reduce_to_22(karma_errors['mother_error_male'] + data['spirituality'])
    family_error_of_money_left =reduce_to_22(karma_errors['mother_error_male'] + data['money'])
    family_error_of_money_right =reduce_to_22(karma_errors['father_error_female'] + data['money'])
    family_error_of_relationship_left =reduce_to_22(karma_errors['father_error_female'] + data['relationship'])
    family_error_of_relationship_right =reduce_to_22(fatal_error['fatal_error'] + data['relationship'])
    family_error_of_health_left =reduce_to_22(fatal_error['fatal_error'] + data['health'])
    family_error_of_health_right =reduce_to_22(karma_errors['mother_error_female'] + data['health'])

    return {
        'family_error_of_personality_left': family_error_of_personality_left,
        'family_error_of_personality_right': family_error_of_personality_right,
        'family_error_of_spirituality_left': family_error_of_spirituality_left,
        'family_error_of_spirituality_right': family_error_of_spirituality_right,
        'family_error_of_money_left': family_error_of_money_left,
        'family_error_of_money_right': family_error_of_money_right,
        'family_error_of_relationship_left': family_error_of_relationship_left,
        'family_error_of_relationship_right': family_error_of_relationship_right,
        'family_error_of_health_left': family_error_of_health_left,
        'family_error_of_health_right': family_error_of_health_right,
    }

family_errors = calculate_family_errors()

def major_error_from_a_past_life():
    error_from_past_of_personality = reduce_to_22(karma_errors['mother_error_female']+karma_errors['father_error_male'])
    error_from_past_of_spirituality = reduce_to_22(karma_errors['father_error_male']+karma_errors['mother_error_male'])
    error_from_past_of_money = reduce_to_22(karma_errors['mother_error_male']+karma_errors['father_error_female'])
    error_from_past_of_relationship = reduce_to_22(karma_errors['father_error_female']+fatal_error['fatal_error'])
    error_from_past_of_health = reduce_to_22(fatal_error['fatal_error']+karma_errors['mother_error_female'])

    return {
        'error_from_past_of_personality': error_from_past_of_personality,
        'error_from_past_of_spirituality': error_from_past_of_spirituality,
        'error_from_past_of_money': error_from_past_of_money,
        'error_from_past_of_relationship': error_from_past_of_relationship,
        'error_from_past_of_health': error_from_past_of_health,
    }

major_error_from_past = major_error_from_a_past_life()


if __name__ == "__main__":

    print(karma_errors)
    print(fatal_error)
    print(family_errors)
    print(major_error_from_past)