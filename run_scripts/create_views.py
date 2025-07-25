from pg.PG import PG

pg = PG(dbname="postgres", user="postgres")


def create_player_view(schema_name: str) -> None:
    pg.create_view(
        schema=schema_name,
        view_name="v_player_data",
        view_query=(
            "SELECT "
            "cw.fpl_player_id as fpl_player_id,"
            "cw.fbref_player_id as fbref_player_id,"
            "fpl_player_data.code as fpl_player_code,"
            "fpl_player_data.web_name as fpl_web_name,"
            "fbref_player_data.team as fbref_team,"
            "CASE "
            "WHEN fpl_player_data.element_type = 1 THEN 'GK' "
            "WHEN fpl_player_data.element_type = 2 THEN 'DEF' "
            "WHEN fpl_player_data.element_type = 3 THEN 'MID' "
            "WHEN fpl_player_data.element_type = 4 THEN 'FWD' "
            "END as fpl_player_position,"
            "ROUND(CAST(fpl_player_data.now_cost AS DECIMAL) / 10,1) as fpl_player_cost,"
            "fpl_player_data.selected_by_percent as fpl_selected_by_percent,"
            "fpl_player_data.minutes as fpl_minutes,"
            "fpl_player_data.total_points as fpl_total_points,"
            "fpl_player_data.goals_scored as fpl_goals_scored,"
            "fpl_player_data.assists as fpl_assists,"
            "fpl_player_data.clean_sheets as fpl_clean_sheets,"
            "fpl_player_data.bonus as fpl_bonus,"
            "fpl_player_data.bps as fpl_bps,"
            "fbref_player_data.xg as fbref_xg,"
            "fbref_player_data.npxg as fbref_npxg,"
            "fbref_player_data.xg_assist as fbref_xg_assist,"
            "fbref_player_data.npxg_xg_assist as fbref_npxg_xg_assist,"
            "CASE "
            "WHEN fpl_player_data.element_type = 1 THEN (fbref_player_data.npxg * 10) + (fbref_player_data.npxg_xg_assist * 3) "  # noqa
            "WHEN fpl_player_data.element_type = 2 THEN (fbref_player_data.npxg * 6) + (fbref_player_data.npxg_xg_assist * 3) "  # noqa
            "WHEN fpl_player_data.element_type = 3 THEN (fbref_player_data.npxg * 5) + (fbref_player_data.npxg_xg_assist * 3) "  # noqa
            "WHEN fpl_player_data.element_type = 4 THEN (fbref_player_data.npxg * 4) + (fbref_player_data.npxg_xg_assist * 3) "  # noqa
            "END as calc_fpl_npxp "
            f"FROM {schema_name}.fpl_player_data fpl_player_data "
            f"JOIN {schema_name}.player_id_crosswalk cw "
            "ON fpl_player_data.fpl_player_id = cw.fpl_player_id "
            f"JOIN {schema_name}.fbref_team_players_standard fbref_player_data "
            "ON fbref_player_data.fbref_player_id = cw.fbref_player_id"
        ),
    )


def create_player_matchlog_view(schema_name: str) -> None:
    pg.create_view(
        schema=schema_name,
        view_name="v_player_matchlog",
        view_query=(
            "SELECT "
            "cw.fpl_player_id as fpl_player_id,"
            "fbref_player_matchlog.round as fbref_round,"
            "fbref_player_matchlog.date as fbref_date,"
            "fbref_player_matchlog.minutes as fbref_minutes,"
            "fbref_player_matchlog.shots as fbref_shots,"
            "fbref_player_matchlog.shots_on_target as fbref_shots_on_target,"
            "fbref_player_matchlog.xg as fbref_xg,"
            "fbref_player_matchlog.npxg as fbref_npxg,"
            "fbref_player_matchlog.xg_assist as fbref_xg_assist,"
            "fpl_player_gameweek_data.round as fpl_gameweek,"
            "CASE "
            "WHEN fpl_player_data.element_type = 1 THEN (fbref_player_matchlog.npxg * 10) + (fbref_player_matchlog.xg_assist * 3) "  # noqa
            "WHEN fpl_player_data.element_type = 2 THEN (fbref_player_matchlog.npxg * 6) + (fbref_player_matchlog.xg_assist * 3) "  # noqa
            "WHEN fpl_player_data.element_type = 3 THEN (fbref_player_matchlog.npxg * 5) + (fbref_player_matchlog.xg_assist * 3) "  # noqa
            "WHEN fpl_player_data.element_type = 4 THEN (fbref_player_matchlog.npxg * 4) + (fbref_player_matchlog.xg_assist * 3) "  # noqa
            "END as calc_fpl_npxp,"
            "CASE "
            "WHEN fpl_player_data.element_type = 1 THEN (fbref_player_matchlog.xg * 10) + (fbref_player_matchlog.xg_assist * 3) "  # noqa
            "WHEN fpl_player_data.element_type = 2 THEN (fbref_player_matchlog.xg * 6) + (fbref_player_matchlog.xg_assist * 3) "  # noqa
            "WHEN fpl_player_data.element_type = 3 THEN (fbref_player_matchlog.xg * 5) + (fbref_player_matchlog.xg_assist * 3) "  # noqa
            "WHEN fpl_player_data.element_type = 4 THEN (fbref_player_matchlog.xg * 4) + (fbref_player_matchlog.xg_assist * 3) "  # noqa
            "END as calc_fpl_xp "
            f"FROM {schema_name}.fpl_player_data fpl_player_data "
            f"JOIN {schema_name}.player_id_crosswalk cw "
            "ON fpl_player_data.fpl_player_id = cw.fpl_player_id "
            f"JOIN {schema_name}.fbref_player_matchlog fbref_player_matchlog "
            "ON fbref_player_matchlog.fbref_player_id = cw.fbref_player_id "
            f"JOIN {schema_name}.fpl_player_gameweek_data fpl_player_gameweek_data "
            "ON fpl_player_gameweek_data.fpl_player_id = cw.fpl_player_id AND fpl_player_gameweek_data.fpl_match_date = fbref_player_matchlog.date"  # noqa
        ),
    )


def create_team_matchlog_view(schema_name: str) -> None:
    pg.create_view(
        schema=schema_name,
        view_name="v_team_matchlog",
        view_query=(
            "SELECT "
            "fbref_team_scores_and_fixtures.team as fbref_team,"
            "fbref_team_scores_and_fixtures.date as fbref_date,"
            "fbref_team_scores_and_fixtures.round as fbref_round "
            f"FROM {schema_name}.fbref_team_scores_and_fixtures fbref_team_scores_and_fixtures "
            "WHERE result IS NOT NULL AND result <> ''"
        ),
    )


def create_views(schema_name: str) -> None:
    create_player_view(schema_name=schema_name)
    create_player_matchlog_view(schema_name=schema_name)
    create_team_matchlog_view(schema_name=schema_name)
