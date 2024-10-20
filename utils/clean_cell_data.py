import re
from typing import Any


def clean_cell_data(cell_value: Any) -> Any:
    if type(cell_value) is str:
        if re.match("^[0-9,]+$", cell_value):
            return cell_value.replace(",", "")
        else:
            return cell_value.replace("'", "''")
    else:
        return cell_value
