from typing import Any


def clean_row_data(
    row_data: list[dict[str, Any]], table_column_config: list[dict[str, Any]]
) -> list[str]:
    cleaned_column_values = []
    for column_data in row_data:
        data_stat = column_data["data_stat"]
        data_stat_config = next(
            item for item in table_column_config if item["column_name"] == data_stat
        )

        if data_stat_config["column_type"] in ("INT", "FLOAT"):
            cleaned_column_values.append(column_data["data_value"].replace(",", ""))
        else:
            cleaned_column_values.append(column_data["data_value"].replace("'", "''"))

    return cleaned_column_values
