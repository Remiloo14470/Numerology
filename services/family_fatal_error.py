from services.reduce_to_22 import reduce_to_22


def calculate_err(error_type: str, userdata) -> dict:
    if error_type == "karma":
        result = calculate_karma_errors(userdata)
    elif error_type == "family":
        result = calculate_family_errors(userdata)
    else:
        raise ValueError("Invalid error type")

    result['error_type'] = error_type
    return result


def calculate_karma_errors(userdata) -> dict:

    """Расчет кармических ошибок."""

    father_error_male = reduce_to_22(userdata.personality + userdata.spirituality)
    mother_error_male = reduce_to_22(userdata.spirituality + userdata.money)
    father_error_female = reduce_to_22(userdata.money  + userdata.relations)
    mother_error_female = reduce_to_22(userdata.health + userdata.personality)
    
    fatal_error = reduce_to_22(userdata.relations + userdata.health)

    return {
        'father_error_male': father_error_male,
        'mother_error_male': mother_error_male,
        'father_error_female': father_error_female,
        'mother_error_female': mother_error_female,
        'fatal_error': fatal_error
    }


def calculate_family_errors(userdata) -> dict:

    familydata = calculate_karma_errors(userdata)

    """Расчет родовых ошибок(ПО БОКАМ ТРЕУГОЛЬНИКОВ) - кармических уроков"""

    family_error_of_personality_left = reduce_to_22(familydata['mother_error_female'] + userdata.personality)
    family_error_of_personality_right =reduce_to_22(familydata['father_error_male'] + userdata.personality)
    family_error_of_spirituality_left =reduce_to_22(familydata['father_error_male'] + userdata.spirituality)
    family_error_of_spirituality_right =reduce_to_22(familydata['mother_error_male'] + userdata.spirituality)
    family_error_of_money_left =reduce_to_22(familydata['mother_error_male'] + userdata.money)
    family_error_of_money_right =reduce_to_22(familydata['father_error_female'] + userdata.money)
    family_error_of_relations_left =reduce_to_22(familydata['father_error_female'] + userdata.relations)
    family_error_of_relations_right =reduce_to_22(familydata['fatal_error'] + userdata.relations)
    family_error_of_health_left =reduce_to_22(familydata['fatal_error'] + userdata.health)
    family_error_of_health_right =reduce_to_22(familydata['mother_error_female'] + userdata.health)

    return {
        'family_error_of_personality_left': family_error_of_personality_left,
        'family_error_of_personality_right': family_error_of_personality_right,
        'family_error_of_spirituality_left': family_error_of_spirituality_left,
        'family_error_of_spirituality_right': family_error_of_spirituality_right,
        'family_error_of_money_left': family_error_of_money_left,
        'family_error_of_money_right': family_error_of_money_right,
        'family_error_of_relations_left': family_error_of_relations_left,
        'family_error_of_relations_right': family_error_of_relations_right,
        'family_error_of_health_left': family_error_of_health_left,
        'family_error_of_health_right': family_error_of_health_right,
    }

#
# def major_error_from_a_past_life(userdata):
#     error_from_past_of_personality = reduce_to_22(userdata.mother_error_female+userdata.father_error_male)
#     error_from_past_of_spirituality = reduce_to_22(userdata.father_error_male+userdata.mother_error_male)
#     error_from_past_of_money = reduce_to_22(userdata.mother_error_male+userdata.father_error_female)
#     error_from_past_of_relations = reduce_to_22(userdata.father_error_female+userdata.fatal_error)
#     error_from_past_of_health = reduce_to_22(userdata.fatal_error+userdata.mother_error_female)
#
#     return {
#         'error_from_past_of_personality': error_from_past_of_personality,
#         'error_from_past_of_spirituality': error_from_past_of_spirituality,
#         'error_from_past_of_money': error_from_past_of_money,
#         'error_from_past_of_relations': error_from_past_of_relations,
#         'error_from_past_of_health': error_from_past_of_health,
#     }


