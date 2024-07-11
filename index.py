from fbref.FBRef_Table import FBRef_Table
from configs.table_configs_merged import merged_table_configs
from configs.run_config import run_configs

from utils.seed_table import seed_table

for run_config in run_configs:
    schema_name: str = run_config["schema_name"]
    table_run_configs: list[dict] = run_config["table_configs"]

    for table_config in table_run_configs:
        table_name = table_config["table_name"]
        table_sql_config = merged_table_configs[table_name]

        fbref_table = FBRef_Table(
            table_url=table_config["table_url"],
            header_row_index=table_config["header_row_index"],
        )

        seed_table(
            schema_name=schema_name,
            table_name=table_name,
            table_column_config=table_sql_config["table_column_configs"],
            table_headers=fbref_table.table_headers,
            table_rows=fbref_table.table_rows,
        )
