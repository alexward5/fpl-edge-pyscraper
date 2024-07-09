from pprint import pprint

from pg.PG import PG
from fbref.FBRef_Table import FBRef_Table
from table_configs_merged import merged_table_configs

SCHEMA_NAME = "TEST_SCHEMA"
TABLE_NAME = "fbref_team_overall"

pg = PG(dbname="postgres", user="postgres")

pg.create_schema(SCHEMA_NAME)
pg.create_table(
    schema=SCHEMA_NAME,
    table_name=TABLE_NAME,
    columns=merged_table_configs[TABLE_NAME]["table_column_sql"],
)

fbref_table = FBRef_Table(
    "https://fbref.com/en/comps/9/Premier-League-Stats",
)

table_headers_str = [header["data_stat"] for header in fbref_table.table_headers]
pprint(table_headers_str)

for table_row in fbref_table.table_rows:
    table_row_values = [f'{row["data_value"]}' for row in table_row]
    pprint(table_row_values)
    pg.insert_row(
        schema=SCHEMA_NAME,
        table_name=TABLE_NAME,
        column_names=table_headers_str,
        row_values=table_row_values,
    )
