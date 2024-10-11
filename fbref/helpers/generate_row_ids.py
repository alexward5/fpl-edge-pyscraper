import uuid

import pandas as pd


def create_unique_id(row, row_id_input_fields):
    values = [str(row[field]) for field in row_id_input_fields]
    concatenated = "".join(values)
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, concatenated))


def generate_row_ids(df: pd.DataFrame, row_id_input_fields: list[str]):
    df["fbref_row_id"] = df.apply(
        lambda row: create_unique_id(row, row_id_input_fields), axis=1
    )
