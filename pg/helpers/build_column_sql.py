from typing import Any


def build_column_sql(column_config: dict[str, Any]) -> str:
    column_sql = f"{column_config["column_name"]} {column_config["column_type"]}"

    if column_config.get('not_null'):
        column_sql = f"{column_sql} NOT NULL"

    if column_config.get('primary_key'):
        column_sql = f"{column_sql} PRIMARY KEY"

    return column_sql
