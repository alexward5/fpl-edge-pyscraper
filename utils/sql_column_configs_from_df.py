import pandas as pd

from utils.fill_df_missing_values import fill_df_missing_values
from utils.set_df_dtypes import set_df_dtypes


def sql_column_configs_from_df(df: pd.DataFrame) -> None:
    set_df_dtypes(df)
    fill_df_missing_values(df)

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
