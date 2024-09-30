from typing import Optional

from configs.run_config import fbref_table_config
from fbref.FBRef_Table import FBRef_Table
from pg.PG import PG
from utils.create_schema_and_tables import create_schema_and_tables
from utils.fbref_table_to_df import fbref_table_to_df
from utils.get_child_table_urls import get_child_table_urls

pg = PG(dbname="postgres", user="postgres")

SCHEMA_NAME = "test_schema"
CREATE_SCHEMA_AND_TABLES = True

if CREATE_SCHEMA_AND_TABLES:
    create_schema_and_tables(schema_name=SCHEMA_NAME)


def process_fbref_table(
    table_url: str, fbref_table_config: dict, parent_field: Optional[dict] = None
):
    fbref_table = FBRef_Table(table_url=table_url, table_config=fbref_table_config)

    fbref_table_df = fbref_table_to_df(
        fbref_table=fbref_table, parent_field=parent_field
    )

    for _, row in fbref_table_df.iterrows():
        pg.insert_row(
            schema=SCHEMA_NAME,
            table_name=fbref_table_config["table_name"],
            column_names=fbref_table_df.columns.to_list(),
            row_values=row.to_list(),
        )

    # If child table config is set, recursively process child tables
    if fbref_table_config.get("child_table_config"):
        child_table_config = fbref_table_config["child_table_config"]
        hyperlink_data_stat = child_table_config["hyperlink_data_stat"]

        child_table_urls = get_child_table_urls(
            fbref_table=fbref_table, hyperlink_data_stat=hyperlink_data_stat
        )

        print(child_table_urls)


process_fbref_table(
    table_url=fbref_table_config["table_url"], fbref_table_config=fbref_table_config
)
