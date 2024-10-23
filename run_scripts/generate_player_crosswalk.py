import csv
import pandas as pd

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from pg.PG import PG
from utils.find_dict_in_list import find_dict_in_list

pg = PG(dbname="postgres", user="postgres")

SCHEMA_NAME = "test_schema_new"


def generate_player_crosswalk() -> None:
    # Create dict of fpl players where each key is a team name and each value is a list of player dicts
    fpl_player_data_by_team: dict[str, list[dict]] = {}

    fpl_player_data = pg.query_table(
        schema=SCHEMA_NAME,
        table_name="fpl_player_data",
        columns=["first_name", "second_name", "fbref_team_name", "fpl_row_id"],
        # Filter out players who have played zero minutes and players who have been removed from game
        where_clause="WHERE minutes > 0 and status != 'u'",
    )

    for fpl_player in fpl_player_data:
        player_dict = dict(fpl_player)
        player_dict["full_name"] = (
            f"{player_dict['first_name']} {player_dict['second_name']}"
        )

        if fpl_player_data_by_team.get(fpl_player["fbref_team_name"]):
            fpl_player_data_by_team[fpl_player["fbref_team_name"]].append(player_dict)
        else:
            fpl_player_data_by_team[fpl_player["fbref_team_name"]] = [player_dict]

    # Create dict of fbref players where each key is a team name and each value is a list of player dicts
    fbref_player_data_by_team: dict[str, list[dict]] = {}

    fbref_player_data = pg.query_table(
        schema=SCHEMA_NAME,
        table_name="fbref_team_players_standard",
        columns=["player as name", "team", "fbref_row_id"],
    )

    for fbref_player in fbref_player_data:
        player_dict = dict(fbref_player)

        if fbref_player_data_by_team.get(fbref_player["team"]):
            fbref_player_data_by_team[fbref_player["team"]].append(player_dict)
        else:
            fbref_player_data_by_team[fbref_player["team"]] = [player_dict]

    # Get custom player name mappings for players who don't match automatically
    player_name_mappings = []
    with open("fpl_api/mappings/player_names.csv", "r") as csvfile:
        dict_reader = csv.DictReader(csvfile)
        player_name_mappings = [row for row in dict_reader]

    # Generate crosswalk
    for team_name in fpl_player_data_by_team:
        fpl_player_data = fpl_player_data_by_team[team_name]
        fbref_player_data = fbref_player_data_by_team[team_name]

        fbref_player_name_list = [player["name"] for player in fbref_player_data]

        # Match fpl player name with fbref player name
        player_id_crosswalk = []
        for fpl_player_dict in fpl_player_data:
            fpl_player_name = fpl_player_dict["full_name"]
            match = process.extractOne(
                fpl_player_name, fbref_player_name_list, scorer=fuzz.token_set_ratio
            )

            if match:
                match_score = match[1]
                # If the match score is less than 70, use custom player name mapping
                if match_score < 70:
                    player_name_mapping = find_dict_in_list(
                        list_of_dicts=player_name_mappings,
                        key="fpl_player_name",
                        value=fpl_player_name,
                    )
                    if not player_name_mapping:
                        raise ValueError(
                            f"Custom player name mapping not found for: {fpl_player_name}"
                        )

                    fbref_player_dict = find_dict_in_list(
                        fbref_player_data,
                        "name",
                        player_name_mapping["fbref_player_name"],
                    )

                    if not fbref_player_dict:
                        raise ValueError(
                            f"FBRef player not found for: {fpl_player_name}"
                        )

                    player_id_crosswalk.append(
                        {
                            "fpl_player_id": fpl_player_dict["fpl_row_id"],
                            "fbref_player_id": fbref_player_dict["fbref_row_id"],
                            "fpl_player_name": fpl_player_name,
                            "fbref_player_name": player_name_mapping[
                                "fbref_player_name"
                            ],
                        }
                    )
                else:
                    fbref_player_dict = find_dict_in_list(
                        fbref_player_data,
                        "name",
                        match[0],
                    )

                    if not fbref_player_dict:
                        raise ValueError(
                            f"FBRef player not found for: {fpl_player_name}"
                        )

                    player_id_crosswalk.append(
                        {
                            "fpl_player_id": fpl_player_dict["fpl_row_id"],
                            "fbref_player_id": fbref_player_dict["fbref_row_id"],
                            "fpl_player_name": fpl_player_name,
                            "fbref_player_name": match[0],
                        }
                    )

        # Create df containing player crosswalk data
        player_id_crosswalk_df = pd.DataFrame(player_id_crosswalk)

        print(player_id_crosswalk_df)
