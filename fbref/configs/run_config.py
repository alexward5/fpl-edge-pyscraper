from typing import Any

fbref_table_config: dict[str, Any] = {
    "table_name": "fbref_team_overall",
    "table_url": "https://fbref.com/en/comps/9/Premier-League-Stats",
    "table_index": 0,
    "header_row_index": 0,
    "row_id_input_fields": ["team"],
    "row_filters": [
        # Rows where expression is True will be filtered from table data
        {"column_name": "team", "comparison": "!=", "value": "Aston Villa"}
    ],
    "filtered_columns": ["last_5", "notes"],
    "child_table_config": {
        "table_name": "fbref_team_players_standard",
        "table_index": 0,
        "header_row_index": 1,
        "row_id_input_fields": ["player", "team"],
        "hyperlink_data_stat": "team",
        "include_parent_fields": "team",
        # "child_table_config": {
        #     "table_name": "fbref_player_matchlog",
        #     "table_index": 0,
        #     "header_row_index": 1,
        #     "hyperlink_data_stat": "matches",
        #     "include_parent_fields": "player",
        #     "row_filters": [
        #         {"column_name": "comp", "comparison": "!=", "value": "Premier League"}
        #     ],
        # },
    },
}
