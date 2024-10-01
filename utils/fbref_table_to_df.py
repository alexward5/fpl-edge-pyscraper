import warnings
from typing import Optional

import numpy as np
import pandas as pd

from fbref.FBRef_Table import FBRef_Table
from utils.clean_cell_data import clean_cell_data


def fbref_table_to_df(
    fbref_table: FBRef_Table,
    parent_field: Optional[dict] = None,
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
    if parent_field:
        # df.assign(**{parent_field["data_stat"]: parent_field["data_value"]})
        df[parent_field["data_stat"]] = parent_field["data_value"]

    # Infer data types of each column
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        df = df.apply(pd.to_numeric, errors="ignore")
    df = df.convert_dtypes()

    # Fill in missing values with zeros for all numeric columns
    for numeric_column in df.select_dtypes(include=np.number).columns:
        df[numeric_column].fillna(0, inplace=True)

    # Fill in remaining missing values with empty strings
    df.fillna("", inplace=True)

    print(df)
    return df
