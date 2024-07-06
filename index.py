from pprint import pprint

# from fbref.FBRef_Table import FBRef_Table

# pprint(
#     FBRef_Table(
#         "https://fbref.com/en/comps/9/Premier-League-Stats",
#     ).table_row_data[1],
#     sort_dicts=False,
# )

from pg.PG import PG
from pg.pg_table_configs.fbref_team_overall import fbref_team_overall

column_configs = {"fbref_team_overall": fbref_team_overall}

SCHEMA_NAME = "TEST_SCHEMA"
TABLE_NAME = "fbref_team_overall"


PG("postgres", "postgres").create_schema(SCHEMA_NAME)
PG("postgres", "postgres").create_table(
    SCHEMA_NAME,
    TABLE_NAME,
    column_configs[TABLE_NAME],
)
