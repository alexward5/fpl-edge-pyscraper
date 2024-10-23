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

    for fbref_player in fpl_players:
        player_dict = dict(fbref_player)
        player_dict["full_name"] = (
            f"{player_dict['first_name']} {player_dict['second_name']}"
        )

        if fpl_players_by_team.get(fbref_player["fbref_team_name"]):
            fpl_players_by_team[fbref_player["fbref_team_name"]].append(player_dict)
        else:
            fpl_players_by_team[fbref_player["fbref_team_name"]] = [player_dict]

    # Create dict of fbref players where each key is a team name and each value is a list of player dicts
    fbref_players_by_team: dict[str, list[dict]] = {}

    fbref_players = pg.query_table(
        schema=SCHEMA_NAME,
        table_name="fbref_team_players_standard",
        columns=["player", "team", "fbref_row_id"],
    )

    for fbref_player in fbref_players:
        player_dict = dict(fbref_player)

        if fbref_players_by_team.get(fbref_player["team"]):
            fbref_players_by_team[fbref_player["team"]].append(player_dict)
        else:
            fbref_players_by_team[fbref_player["team"]] = [player_dict]

    print(fpl_players_by_team["Arsenal"])
