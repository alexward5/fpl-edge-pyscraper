from typing import Optional

from configs.run_config import fbref_table_config
from configs.table_configs_merged import merged_table_configs
from fbref.FBRef_Table import FBRef_Table
from utils.seed_table import seed_table

schema_name = "test_schema"


def recursive_run(
    fbref_table_config: dict, table_url: str = "", parent_field: Optional[dict] = None
):
    table_name = fbref_table_config["table_name"]
    table_config = merged_table_configs[table_name]

    table_url = fbref_table_config.get("table_url") or table_url

    fbref_table = FBRef_Table(
        table_url=table_url, table_config=fbref_table_config, custom_column=parent_field
    )

    seed_table(
        schema_name=schema_name,
        table_name=table_name,
        table_column_configs=table_config["table_column_configs"],
        table_headers=fbref_table.table_headers,
        table_rows=fbref_table.table_rows,
    )

    sub_tables_metadata: list[dict] = []
    if fbref_table_config.get("sub_table_config"):
        sub_table_config = fbref_table_config["sub_table_config"]
        hyperlink_data_stat = sub_table_config["hyperlink_data_stat"]

        for row_data in fbref_table.table_rows:
            sub_table_metadata = {}

            hyperlink_cell = next(
                item for item in row_data if item["data_stat"] == hyperlink_data_stat
            )

            if hyperlink_cell.get("data_hyperlink"):
                sub_table_metadata["data_hyperlink"] = hyperlink_cell["data_hyperlink"]

            if sub_table_config.get("include_parent_field"):
                parent_field_data_stat = sub_table_config["include_parent_field"]
                parent_field_cell = next(
                    item
                    for item in row_data
                    if item["data_stat"] == parent_field_data_stat
                )

                sub_table_metadata["parent_field"] = {
                    "data_stat": parent_field_cell["data_stat"],
                    "data_value": parent_field_cell["data_value"],
                }

            if sub_table_metadata.get("data_hyperlink"):
                sub_tables_metadata.append(sub_table_metadata)

        if sub_tables_metadata:
            for sub_table_metadata in sub_tables_metadata:
                run_args = {
                    "fbref_table_config": fbref_table_config["sub_table_config"],
                    "table_url": sub_table_metadata["data_hyperlink"],
                }

                if sub_table_config.get("include_parent_field"):
                    run_args["parent_field"] = sub_table_metadata["parent_field"]

                recursive_run(**run_args)


recursive_run(fbref_table_config=fbref_table_config)
