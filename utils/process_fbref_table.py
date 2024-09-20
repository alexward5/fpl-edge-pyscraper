import pandas as pd
from fbref.FBRef_Table import FBRef_Table


def process_fbref_table(table_url: str, fbref_table_config: dict):
    fbref_table = FBRef_Table(table_url=table_url, table_config=fbref_table_config)

    # Create pandas dataframe using data from fbref table
    df_dict: dict[str, list] = {}

    for table_row in fbref_table.table_rows:
        for table_cell in table_row:
            data_stat = table_cell["data_stat"]
            data_value = table_cell["data_value"]

            if df_dict.get(data_stat):
                df_dict[data_stat].append(data_value)
            else:
                df_dict[data_stat] = [data_value]

    df = pd.DataFrame.from_dict(df_dict)

    # Infer data types of each column and fill in missing values
    df = df.apply(pd.to_numeric, errors="ignore")
    df = df.convert_dtypes()
    df = df.fillna(df)

    print(df.dtypes)
