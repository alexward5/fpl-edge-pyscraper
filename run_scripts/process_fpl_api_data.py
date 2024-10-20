import pandas as pd

from fpl_api.FPL_API import FPL_API
from pg.PG import PG
from utils.clean_cell_data import clean_cell_data
from utils.set_df_dtypes import set_df_dtypes

pg = PG(dbname="postgres", user="postgres")


def process_fpl_api_data() -> None:
    fpl_api_data = FPL_API()

    fpl_players_df = pd.DataFrame.from_records(fpl_api_data.player_data)
    fpl_players_df = set_df_dtypes(fpl_players_df)

    # Insert dataframe rows into postgres table
    for _, row in fpl_players_df.iterrows():
        cleaned_row_values = [clean_cell_data(val) for val in row.to_list()]

        pg.insert_row(
            schema="test_schema_new",
            table_name="fpl_player_data",
            column_names=fpl_players_df.columns.to_list(),
            row_values=cleaned_row_values,
        )
