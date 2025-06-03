from datetime import date
from services.destiny_potential_matrix import calculate_destiny_matrix
from services.family_fatal_error import calculate_family_errors, calculate_karma_errors


class UserDataMatrix:
    def __init__(self, matrix: dict):
        self.personality = matrix["personality"]
        self.spirituality = matrix["spirituality"]
        self.money = matrix["money"]
        self.relations = matrix["relations"]
        self.health = matrix["health"]
        self.soul_mission = matrix["soul_mission"]


def calc_partners_numbers(birth_date: date) -> dict:
    partner_matrix = calculate_destiny_matrix(birth_date=birth_date)
    userdata = UserDataMatrix(partner_matrix)

    partner_karma = calculate_karma_errors(userdata)
    partner_family = calculate_family_errors(userdata)

    return {
        "partner_matrix": partner_matrix,
        "partner_karma": partner_karma,
        "partner_family": partner_family
    }