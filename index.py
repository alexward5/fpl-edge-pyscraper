from pprint import pprint

# from fbref.FBRef_Table import FBRef_Table

# pprint(
#     FBRef_Table(
#         "https://fbref.com/en/comps/9/Premier-League-Stats",
#     ).table_row_data[1],
#     sort_dicts=False,
# )

from pg.PG import PG
from table_configs.table_configs import table_configs

SCHEMA_NAME = "TEST_SCHEMA"
TABLE_NAME = "fbref_team_overall"

pg = PG(dbname="postgres", user="postgres")

pg.create_schema(SCHEMA_NAME)
pg.create_table(
    schema=SCHEMA_NAME,
    table_name=TABLE_NAME,
    columns=table_configs["table_column_sql"][TABLE_NAME],
)
