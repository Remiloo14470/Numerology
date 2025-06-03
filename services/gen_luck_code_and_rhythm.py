from services.reduce_to_22 import reduce_to_22


def calculate_luck_code(personal_year: int) -> dict:
    stability_code = reduce_to_22(personal_year + 4)
    prosperity_code = reduce_to_22(personal_year + 8)
    return {
        "stability_code": stability_code,
        "prosperity_code": prosperity_code,
    }


def calculate_luck_rhythm(personal_year: int, destiny_number: int) -> dict:
    luck_rhythm = reduce_to_22(personal_year + destiny_number)
    return {"luck_rhythm": luck_rhythm}

