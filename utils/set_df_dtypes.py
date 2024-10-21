import warnings

import pandas as pd


def set_df_dtypes(df: pd.DataFrame) -> None:
    # Infer data types of each column
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        df = df.apply(pd.to_numeric, errors="ignore")
    df = df.convert_dtypes()
