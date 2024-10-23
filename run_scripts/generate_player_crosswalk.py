import pandas as pd

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from pg.PG import PG

pg = PG(dbname="postgres", user="postgres")

SCHEMA_NAME = "test_schema_new"


def generate_player_crosswalk() -> None:
    # Create dict of fpl players where each key is a team name and each value is a list of player dicts
    fpl_players_by_team: dict[str, list[dict]] = {}

    fpl_players = pg.query_table(
        schema=SCHEMA_NAME,
        table_name="fpl_player_data",
        columns=["first_name", "second_name", "fbref_team_name", "fpl_row_id"],
    )

    for fpl_player in fpl_players:
        player_dict = dict(fpl_player)
        player_dict["full_name"] = (
            f"{player_dict['first_name']} {player_dict['second_name']}"
        )

        if fpl_players_by_team.get(fpl_player["fbref_team_name"]):
            fpl_players_by_team[fpl_player["fbref_team_name"]].append(player_dict)
        else:
            fpl_players_by_team[fpl_player["fbref_team_name"]] = [player_dict]

    # Create dict of fbref players where each key is a team name and each value is a list of player dicts
    fbref_players_by_team: dict[str, list[dict]] = {}

    fbref_players = pg.query_table(
        schema=SCHEMA_NAME,
        table_name="fbref_team_players_standard",
        columns=["player as name", "team", "fbref_row_id"],
    )

    for fbref_player in fbref_players:
        player_dict = dict(fbref_player)

        if fbref_players_by_team.get(fbref_player["team"]):
            fbref_players_by_team[fbref_player["team"]].append(player_dict)
        else:
            fbref_players_by_team[fbref_player["team"]] = [player_dict]

    # Generate crosswalk
    for team_name in fpl_players_by_team:
        if team_name != "Aston Villa":
            continue

        fpl_player_name_list = [
            player["full_name"]
            for player in fpl_players_by_team[team_name]
            if player["fbref_team_name"] == team_name
        ]
        fbref_player_name_list = [
            player["name"]
            for player in fbref_players_by_team[team_name]
            if player["team"] == team_name
        ]

        # Perform fuzzy matching
        matches = []
        for item in fpl_player_name_list:
            match = process.extractOne(
                item, fbref_player_name_list, scorer=fuzz.token_set_ratio
            )
            if match:
                match_score = match[1]
                matches.append([item, match[0], match_score])

        # Convert the output to pandas df
        df = pd.DataFrame(
            matches, columns=["fpl_player_name", "fbref_player_name", "score"]
        )

        df_sorted = df.sort_values(by=["score"])

        # Print the DataFrame
        print(df_sorted)
