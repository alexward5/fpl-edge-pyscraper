import pandas as pd

from fpl_api.FPL_API import FPL_API
from pg.configs.table_configs.fpl_player_data import (
    fpl_player_data as fpl_player_data_config,
)
from pg.PG import PG
from utils.clean_cell_data import clean_cell_data
from utils.fill_df_missing_values import fill_df_missing_values
from utils.generate_row_ids import generate_row_ids
from utils.set_df_dtypes import set_df_dtypes

pg = PG(dbname="postgres", user="postgres")


def process_fpl_api_data(schema_name: str) -> None:
    fpl_player_data_column_configs = fpl_player_data_config["table_column_configs"]
    fpl_player_data_column_names = [
        column_config["column_name"] for column_config in fpl_player_data_column_configs
    ]

    fpl_api_data = FPL_API()

    fpl_players_df = pd.DataFrame.from_records(fpl_api_data.player_data)

    # Drop columns from df that are not in table column config
    for col in fpl_players_df.columns:
        if col not in fpl_player_data_column_names:
            fpl_players_df = fpl_players_df.drop(col, axis=1)

    fpl_players_df = set_df_dtypes(fpl_players_df)
    fpl_players_df = fill_df_missing_values(fpl_players_df)
    fpl_players_df = generate_row_ids(
        df=fpl_players_df,
        row_id_input_fields=["first_name", "second_name", "fbref_team_name"],
        row_id_column_name="fpl_player_id",
    )

    # Insert dataframe rows into postgres table
    for _, row in fpl_players_df.iterrows():
        cleaned_row_values = [clean_cell_data(val) for val in row.to_list()]

        pg.insert_row(
            schema=schema_name,
            table_name="fpl_player_data",
            column_names=fpl_players_df.columns.to_list(),
            row_values=cleaned_row_values,
            update_on="fpl_player_id",
        )
