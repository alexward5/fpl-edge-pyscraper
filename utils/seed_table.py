from pg.PG import PG
from utils.build_column_sql import build_column_sql
from utils.clean_row_data import clean_row_data


def seed_table(
    schema_name: str,
    table_name: str,
    table_column_configs: list,
    table_headers: list,
    table_rows: list,
):

    pg = PG(dbname="postgres", user="postgres")

    pg.create_schema(schema_name=schema_name)
    pg.create_table(
        schema=schema_name,
        table_name=table_name,
        columns=[
            build_column_sql(column_config) for column_config in table_column_configs
        ],
    )

    table_headers_list = [header["data_stat"] for header in table_headers]

    for table_row in table_rows:
        cleaned_row_values = clean_row_data(table_row, table_column_configs)

        pg.insert_row(
            schema=schema_name,
            table_name=table_name,
            column_names=table_headers_list,
            row_values=cleaned_row_values,
        )

    print(f"Finished inserting rows into: {table_name}")
