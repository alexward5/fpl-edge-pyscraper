import warnings

import numpy as np
import pandas as pd

from fbref.FBRef_Table import FBRef_Table


def fbref_table_to_df(table_url: str, fbref_table_config: dict):
    fbref_table = FBRef_Table(table_url=table_url, table_config=fbref_table_config)

    # Create pandas dataframe using data from fbref table
    df_dict: dict[str, list] = {}

    for table_row in fbref_table.table_rows:
        for table_cell in table_row:
            data_stat = table_cell["data_stat"]

            # Add hyperlink to dataframe if hyperlink_data_stat is set in config
            if data_stat == fbref_table_config.get("hyperlink_data_stat"):
                data_value = table_cell.get("data_hyperlink") or ""
            else:
                data_value = table_cell["data_value"]

            # Create key for data stat in df dict, unless it already exists
            if df_dict.get(data_stat):
                df_dict[data_stat].append(data_value)
            else:
                df_dict[data_stat] = [data_value]

    df = pd.DataFrame.from_dict(df_dict)

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
