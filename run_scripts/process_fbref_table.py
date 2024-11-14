from typing import Optional

from fbref.FBRef_Table import FBRef_Table
from fbref.helpers.fbref_table_to_df import fbref_table_to_df
from fbref.helpers.get_child_table_urls import get_child_table_urls
from pg.PG import PG
from utils.generate_row_ids import generate_row_ids

pg = PG(dbname="postgres", user="postgres")


def process_fbref_table(
    schema_name: str,
    table_url: str,
    fbref_table_config: dict,
    parent_fields: Optional[list[dict]] = None,
):
    fbref_table = FBRef_Table(table_url=table_url, table_config=fbref_table_config)

    # Create pandas dataframe using data from fbref table
    fbref_table_df = fbref_table_to_df(
        fbref_table=fbref_table, parent_fields=parent_fields
    )

    # If configured, generate unique ids for each row in dataframe using row id input fields
    if fbref_table_config.get("row_id_config"):
        fbref_table_df = generate_row_ids(
            df=fbref_table_df,
            row_id_input_fields=fbref_table_config["row_id_config"][
                "row_id_input_fields"
            ],
            row_id_column_name=fbref_table_config["row_id_config"]["column_name"],
        )

    print(fbref_table_df)

    # Insert dataframe rows into postgres table
    for _, row in fbref_table_df.iterrows():
        pg.insert_row(
            schema=schema_name,
            table_name=fbref_table_config["table_name"],
            column_names=fbref_table_df.columns.to_list(),
            row_values=row.to_list(),
        )

    # If child table config is set, recursively process child tables
    if fbref_table_config.get("child_table_config"):
        child_table_config = fbref_table_config["child_table_config"]
        hyperlink_data_stat = child_table_config["hyperlink_data_stat"]

        # Get child table URLs from parent table hyperlinks
        child_table_urls = get_child_table_urls(
            fbref_table=fbref_table, hyperlink_data_stat=hyperlink_data_stat
        )

        # For each child table URL, recursively process child table
        for index, child_table_url in enumerate(child_table_urls):
            run_args = {
                "schema_name": schema_name,
                "table_url": child_table_url,
                "fbref_table_config": child_table_config,
            }

            # Add parent fields to run args if set in config
            parent_fields = []
            if child_table_config.get("include_parent_fields"):
                parent_fields.append(
                    {
                        "data_stat": child_table_config["include_parent_fields"],
                        "data_value": fbref_table_df.loc[
                            index, child_table_config["include_parent_fields"]
                        ],
                    }
                )

            run_args["parent_fields"] = parent_fields

            process_fbref_table(**run_args)
