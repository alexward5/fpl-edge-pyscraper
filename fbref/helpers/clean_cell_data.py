import re


def clean_cell_data(input_str: str) -> str:
    if re.match("^[0-9,]+$", input_str):
        return input_str.replace(",", "")
    else:
        return input_str.replace("'", "''")
