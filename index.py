from fbref.FBRef_Table import FBRef_Table
from pg.PG import PG
from configs.table_configs_merged import merged_table_configs
from utils.build_column_sql import build_column_sql
from utils.clean_row_data import clean_row_data


def seed_table(schema_name: str, table_name: str, table_url: str):
    table_config = merged_table_configs[table_name]
    table_column_config = table_config["table_column_configs"]

    fbref_table = FBRef_Table(
        table_url=table_url, header_row_index=table_config["header_row_index"]
    )
    pg = PG(dbname="postgres", user="postgres")

    pg.create_schema(schema_name=schema_name)
    pg.create_table(
        schema=schema_name,
        table_name=table_name,
        columns=[
            build_column_sql(column_config) for column_config in table_column_config
        ],
    )

    table_headers_list = [header["data_stat"] for header in fbref_table.table_headers]

    for table_row in fbref_table.table_rows:
        cleaned_row_values = clean_row_data(table_row, table_column_config)

        # Filter rows at bottom of table containing sum totals
        sum_total_row = False
        for row_value in cleaned_row_values:
            if "total" in row_value.lower():
                sum_total_row = True
                break

        if not sum_total_row:
            pg.insert_row(
                schema=schema_name,
                table_name=table_name,
                column_names=table_headers_list,
                row_values=cleaned_row_values,
            )


seed_table(
    schema_name="test_schema",
    table_name="fbref_team_standard",
    table_url="https://fbref.com/en/squads/18bb7c10/2023-2024/Arsenal-Stats",
)
