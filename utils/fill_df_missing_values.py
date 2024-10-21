import numpy as np
import pandas as pd


def fill_df_missing_values(df: pd.DataFrame) -> None:
    # Fill in missing values with zeros for all numeric columns
    for numeric_column in df.select_dtypes(include=np.number).columns:
        df[numeric_column] = df[numeric_column].fillna(0)

    # Fill in remaining missing values with empty strings
    df = df.fillna("")
