from pg.PG import PG

pg = PG(dbname="postgres", user="postgres")

SCHEMA_NAME = "test_schema_new"


def create_player_views() -> None:
    pg.create_view(
        schema=SCHEMA_NAME,
        view_name="v_player_data",
        view_query=(
            "SELECT "
            "fpl_player_data.code as fpl_player_code,"
            "fpl_player_data.element_type as fpl_player_position,"
            "ROUND(CAST(fpl_player_data.now_cost AS DECIMAL) / 10,1) as fpl_player_cost,"
            "fpl_player_data.selected_by_percent as fpl_selected_by_percent,"
            "fpl_player_data.total_points as fpl_total_points,"
            "fpl_player_data.goals_scored as fpl_goals_scored,"
            "fpl_player_data.assists as fpl_assists,"
            "fpl_player_data.clean_sheets as fpl_clean_sheets,"
            "fpl_player_data.goals_conceded as fpl_goals_conceded,"
            "fpl_player_data.bonus as fpl_bonus,"
            "fpl_player_data.bps as fpl_bps,"
            "fpl_player_data.expected_goals_conceded as fpl_expected_goals_conceded,"
            "fbref_player_data.player as fbref_name,"
            "fbref_player_data.team as fbref_team,"
            "fbref_player_data.age as fbref_age,"
            "fbref_player_data.xg as fbref_xg,"
            "fbref_player_data.npxg as fbref_npxg,"
            "fbref_player_data.xg_assist as fbref_xg_assist,"
            "fbref_player_data.npxg_xg_assist as fbref_npxg_xg_assist,"
            "fbref_player_data.progressive_carries as fbref_progressive_carries,"
            "fbref_player_data.progressive_passes as fbref_progressive_passes,"
            "fbref_player_data.progressive_passes_received as fbref_progressive_passes_received "
            f"FROM {SCHEMA_NAME}.fpl_player_data fpl_player_data "
            f"JOIN {SCHEMA_NAME}.player_id_crosswalk cw "
            "ON fpl_player_data.fpl_row_id = cw.fpl_player_id "
            f"JOIN {SCHEMA_NAME}.fbref_team_players_standard fbref_player_data "
            "ON fbref_player_data.fbref_row_id = cw.fbref_player_id"
        ),
    )


def create_views() -> None:
    create_player_views()
