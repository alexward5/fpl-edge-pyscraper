import warnings

import numpy as np
import pandas as pd


def set_df_dtypes(df: pd.DataFrame) -> pd.DataFrame:
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

    return df
