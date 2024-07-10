from fbref.FBRef_Table import FBRef_Table
from pg.PG import PG
from table_configs_merged import merged_table_configs
from utils.build_column_sql import build_column_sql
from utils.clean_row_data import clean_row_data


SCHEMA_NAME = "test_schema"
TABLE_NAME = "fbref_team_overall"

pg = PG(dbname="postgres", user="postgres")

table_column_config = merged_table_configs[TABLE_NAME]["table_column_configs"]

pg.create_schema(schema_name=SCHEMA_NAME)
pg.create_table(
    schema=SCHEMA_NAME,
    table_name=TABLE_NAME,
    columns=[build_column_sql(column_config) for column_config in table_column_config],
)

fbref_table = FBRef_Table(
    "https://fbref.com/en/comps/9/Premier-League-Stats",
)

table_headers_list = [header["data_stat"] for header in fbref_table.table_headers]

for table_row in fbref_table.table_rows:
    cleaned_row_values = clean_row_data(table_row, table_column_config)

    pg.insert_row(
        schema=SCHEMA_NAME,
        table_name=TABLE_NAME,
        column_names=table_headers_list,
        row_values=cleaned_row_values,
    )
