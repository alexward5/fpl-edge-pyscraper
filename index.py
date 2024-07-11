from fbref.FBRef_Table import FBRef_Table
from configs.table_configs_merged import merged_table_configs

from utils.seed_table import seed_table


table_config = merged_table_configs["fbref_team_standard"]

fbref_table = FBRef_Table(
    table_url="https://fbref.com/en/squads/18bb7c10/2023-2024/Arsenal-Stats",
    header_row_index=table_config["header_row_index"],
)


seed_table(
    schema_name="test_schema",
    table_name="fbref_team_standard",
    table_column_config=table_config["table_column_configs"],
    table_headers=fbref_table.table_headers,
    table_rows=fbref_table.table_rows,
)
