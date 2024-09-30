import re


def remove_commas_from_numbers(input_str: str) -> str:
    if re.match("^[0-9,]+$", input_str):
        return input_str.replace(",", "")
    else:
        return input_str
