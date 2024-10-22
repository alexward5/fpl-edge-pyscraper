from pg.PG import PG

pg = PG(dbname="postgres", user="postgres")

SCHEMA_NAME = "test_schema_new"


def generate_player_crosswalk() -> None:
    fbref_players = pg.query_table(
        schema=SCHEMA_NAME,
        table_name="fbref_team_players_standard",
        columns=["player", "team", "fbref_row_id"],
    )

    fbref_players_by_team: dict[str, list[dict]] = {}
    for fbref_player in fbref_players:
        player_dict = dict(fbref_player)

        if fbref_players_by_team.get(fbref_player["team"]):
            fbref_players_by_team[fbref_player["team"]].append(player_dict)
        else:
            fbref_players_by_team[fbref_player["team"]] = [player_dict]

    print(fbref_players_by_team["Arsenal"])
