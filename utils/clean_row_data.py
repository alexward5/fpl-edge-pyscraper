from typing import Any


def clean_row_data(
    row_data: list[dict[str, Any]], table_column_config: list[dict[str, Any]]
) -> list[str]:
    if len(row_data) != len(table_column_config):
        raise ValueError(
            f"Table column count ({len(row_data)}) does not match config column count ({len(table_column_config)})"
        )

    cleaned_cell_values = []
    for cell_data in row_data:
        data_stat = cell_data["data_stat"]
        data_value = cell_data["data_value"]

        column_config = next(
            item for item in table_column_config if item["column_name"] == data_stat
        )

        if column_config["column_type"] in ("INT", "DECIMAL"):
            if data_value:
                cleaned_cell_values.append(data_value.replace(",", ""))
            else:
                cleaned_cell_values.append("0")
        else:
            cleaned_cell_values.append(data_value.replace("'", "''"))

    return cleaned_cell_values
