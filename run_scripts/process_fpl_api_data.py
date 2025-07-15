import pandas as pd

from fpl_api.FPL_API import FPL_API
from pg.configs.table_configs.fpl_player_data import (
    fpl_player_data as fpl_player_data_config,
)
from pg.configs.table_configs.fpl_player_gameweek_data import (
    fpl_player_gameweek_data as fpl_player_gameweek_data_config,
)
from pg.configs.table_configs.fpl_events import fpl_events as fpl_events_config
from pg.PG import PG
from utils.clean_cell_data import clean_cell_data
from utils.fill_df_missing_values import fill_df_missing_values
from utils.generate_row_ids import generate_row_ids
from utils.set_df_dtypes import set_df_dtypes

pg = PG(dbname="postgres", user="postgres")


def process_fpl_player_data(schema_name: str) -> None:
    fpl_player_data_column_configs = fpl_player_data_config["table_column_configs"]
    fpl_player_data_column_names = [
        column_config["column_name"] for column_config in fpl_player_data_column_configs
    ]

    fpl_api_data = FPL_API()

    fpl_players_df = pd.DataFrame.from_records(fpl_api_data.player_data)

    fpl_players_df["fbref_team_name"] = fpl_players_df["id"].map(
        fpl_api_data.team_id_mapping
    )

    fpl_players_df = set_df_dtypes(fpl_players_df)
    fpl_players_df = fill_df_missing_values(fpl_players_df)
    fpl_players_df = generate_row_ids(
        df=fpl_players_df,
        row_id_input_fields=["first_name", "second_name", "fbref_team_name"],
        row_id_column_name="fpl_player_id",
    )

    # Drop columns from df that are not in table column config
    for col in fpl_players_df.columns:
        if col not in fpl_player_data_column_names:
            fpl_players_df = fpl_players_df.drop(col, axis=1)

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


def process_fpl_player_gameweek_data(schema_name: str) -> None:
    fpl_player_gameweek_data_column_configs = fpl_player_gameweek_data_config[
        "table_column_configs"
    ]
    fpl_player_gameweek_data_column_names = [
        column_config["column_name"]
        for column_config in fpl_player_gameweek_data_column_configs
    ]

    fpl_api_data = FPL_API()

    fpl_players_df = pd.DataFrame.from_records(fpl_api_data.get_player_gameweek_data())

    # Add 3 fields needed to create unique player id
    fpl_players_df["first_name"] = fpl_players_df["element"].map(
        lambda x: fpl_api_data.player_id_mapping[x]["first_name"]
    )
    fpl_players_df["second_name"] = fpl_players_df["element"].map(
        lambda x: fpl_api_data.player_id_mapping[x]["second_name"]
    )
    fpl_players_df["fbref_team_name"] = fpl_players_df["element"].map(
        lambda x: fpl_api_data.player_id_mapping[x]["fbref_team_name"]
    )

    fpl_players_df = set_df_dtypes(fpl_players_df)
    fpl_players_df = fill_df_missing_values(fpl_players_df)
    fpl_players_df = generate_row_ids(
        df=fpl_players_df,
        row_id_input_fields=["first_name", "second_name", "fbref_team_name"],
        row_id_column_name="fpl_player_id",
    )

    # Create unique row id for each player/gameweek
    fpl_players_df = generate_row_ids(
        df=fpl_players_df,
        row_id_input_fields=["fpl_player_id", "fixture"],
        row_id_column_name="fpl_player_gameweek_id",
    )

    # Create custom date field using kickoff timestamp
    fpl_players_df["fpl_match_date"] = (
        fpl_players_df["kickoff_time"].str.split("T").str[0]
    )

    # Drop columns from df that are not in table column config
    for col in fpl_players_df.columns:
        if col not in fpl_player_gameweek_data_column_names:
            fpl_players_df = fpl_players_df.drop(col, axis=1)

    # Insert dataframe rows into postgres table
    for _, row in fpl_players_df.iterrows():
        cleaned_row_values = [clean_cell_data(val) for val in row.to_list()]

        pg.insert_row(
            schema=schema_name,
            table_name="fpl_player_gameweek_data",
            column_names=fpl_players_df.columns.to_list(),
            row_values=cleaned_row_values,
            update_on="fpl_player_gameweek_id",
        )


def process_fpl_events(schema_name: str) -> None:
    fpl_events_column_configs = fpl_events_config["table_column_configs"]
    fpl_events_column_names = [
        column_config["column_name"] for column_config in fpl_events_column_configs
    ]

    fpl_api_data = FPL_API()
    fpl_events_df = pd.DataFrame.from_records(fpl_api_data.events_data)

    fpl_events_df = set_df_dtypes(fpl_events_df)
    fpl_events_df = fill_df_missing_values(fpl_events_df)

    # Drop columns from df that are not in table column config
    for col in fpl_events_df.columns:
        if col not in fpl_events_column_names:
            fpl_events_df = fpl_events_df.drop(col, axis=1)

    # Insert dataframe rows into postgres table
    for _, row in fpl_events_df.iterrows():
        cleaned_row_values = [clean_cell_data(val) for val in row.to_list()]

        pg.insert_row(
            schema=schema_name,
            table_name="fpl_events",
            column_names=fpl_events_df.columns.to_list(),
            row_values=cleaned_row_values,
            update_on="id",
        )


def process_fpl_api_data(schema_name: str) -> None:
    process_fpl_player_data(schema_name=schema_name)
    process_fpl_player_gameweek_data(schema_name=schema_name)
    process_fpl_events(schema_name=schema_name)
