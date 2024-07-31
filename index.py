from time import sleep

from configs.run_config import fbref_table_config
from configs.table_configs_merged import merged_table_configs
from fbref.FBRef_Table import FBRef_Table
from utils.seed_table import seed_table

schema_name = "test_schema"


def recursive_run(fbref_table_config: dict, table_url: str = ""):
    table_name = fbref_table_config["table_name"]
    table_config = merged_table_configs[table_name]

    table_url = fbref_table_config.get("table_url") or table_url

    fbref_table = FBRef_Table(
        table_url=table_url,
        table_config=fbref_table_config,
    )

    # Sleep for 10s between runs to avoid reaching rate limit
    sleep(10)

    seed_table(
        schema_name=schema_name,
        table_name=table_name,
        table_column_configs=table_config["table_column_configs"],
        table_headers=fbref_table.table_headers,
        table_rows=fbref_table.table_rows,
    )

    sub_table_urls = []
    if fbref_table_config.get("sub_table_config"):
        sub_table_config = fbref_table_config["sub_table_config"]
        hyperlink_data_stat = sub_table_config["hyperlink_data_stat"]

        for row_data in fbref_table.table_rows:
            hyperlink_cell = next(
                item for item in row_data if item["data_stat"] == hyperlink_data_stat
            )

            sub_table_urls.append(hyperlink_cell["data_hyperlink"])

    if sub_table_urls:
        for sub_table_url in sub_table_urls:
            recursive_run(
                fbref_table_config["sub_table_config"], table_url=sub_table_url
            )


recursive_run(fbref_table_config=fbref_table_config)
