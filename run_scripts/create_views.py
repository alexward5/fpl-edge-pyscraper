from pg.PG import PG

pg = PG(dbname="postgres", user="postgres")

SCHEMA_NAME = "test_schema_new"


def create_player_views() -> None:
    pg.create_view(
        schema=SCHEMA_NAME,
        view_name="v_player_data",
        view_query=(
            "SELECT fpl_player_data.now_cost, fbref_player_data.* "
            f"FROM {SCHEMA_NAME}.fpl_player_data fpl_player_data "
            f"JOIN {SCHEMA_NAME}.player_id_crosswalk cw "
            "ON fpl_player_data.fpl_row_id = cw.fpl_player_id "
            f"JOIN {SCHEMA_NAME}.fbref_team_players_standard fbref_player_data "
            "ON fbref_player_data.fbref_row_id = cw.fbref_player_id"
        ),
    )


def create_views() -> None:
    create_player_views()
