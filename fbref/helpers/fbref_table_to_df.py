from typing import Optional

import pandas as pd

from fbref.FBRef_Table import FBRef_Table
from utils.clean_cell_data import clean_cell_data


def fbref_table_to_df(
    fbref_table: FBRef_Table,
    parent_fields: Optional[list[dict]] = None,
):
    # Create pandas dataframe using data from fbref table
    df_dict: dict[str, list] = {}

    for table_row in fbref_table.table_rows:
        for table_cell in table_row:
            data_stat = table_cell["data_stat"]
            data_value = clean_cell_data(table_cell["data_value"])

            # Create key for data stat in df dict, or if it already exists append value to list
            if df_dict.get(data_stat):
                df_dict[data_stat].append(data_value)
            else:
                df_dict[data_stat] = [data_value]

    df = pd.DataFrame.from_dict(df_dict)

    # Add parent field to new column in dataframe
    if parent_fields:
        for parent_field in parent_fields:
            df[parent_field["data_stat"]] = parent_field["data_value"]

    return df
