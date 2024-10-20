import warnings

import numpy as np
import pandas as pd


def sql_column_configs_from_df(df: pd.DataFrame) -> None:
    # Infer data types of each column
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        df = df.apply(pd.to_numeric, errors="ignore")
    df = df.convert_dtypes()

    # Fill in missing values with zeros for all numeric columns
    for numeric_column in df.select_dtypes(include=np.number).columns:
        df[numeric_column] = df[numeric_column].fillna(0)

    # Fill in remaining missing values with empty strings
    df = df.fillna("")

    temp = []
    for column, dtype in df.dtypes.items():
        dtype = str(dtype)
        sql_column_type = ""
        if dtype == "Int64":
            sql_column_type = "INT"
        elif dtype == "float64":
            sql_column_type = "DECIMAL"
        elif dtype == "boolean":
            sql_column_type = "BOOLEAN"
        else:
            sql_column_type = "VARCHAR (255)"

        temp.append(
            {
                "column_name": column,
                "column_type": sql_column_type,
                "not_null": True,
            }
        )

    print(temp)
