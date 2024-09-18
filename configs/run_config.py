from typing import Any

fbref_table_config: dict[str, Any] = {
    "table_name": "fbref_team_overall",
    "table_url": "https://fbref.com/en/comps/9/Premier-League-Stats",
    "table_index": 0,
    "header_row_index": 0,
    "row_filters": [
        # Rows where expression is True will be filtered from table data
        # {"column_name": "team", "comparison": "!=", "value": "Manchester Utd"}
    ],
    "filtered_columns": ["last_5"],
    "sub_table_config": {
        "table_name": "fbref_team_players_standard",
        "table_index": 0,
        "header_row_index": 1,
        "hyperlink_data_stat": "team",
        "include_parent_field": "team",
        # "sub_table_config": {
        #     "table_name": "fbref_player_matchlog",
        #     "table_index": 0,
        #     "header_row_index": 1,
        #     "hyperlink_data_stat": "matches",
        #     "include_parent_field": "player",
        #     "row_filters": [
        #         {"column_name": "comp", "comparison": "!=", "value": "Premier League"}
        #     ],
        # },
    },
}

# fbref_table_config: dict[str, Any] = {
#     "table_name": "fbref_player_matchlog",
#     "table_url": "https://fbref.com/en/players/972aeb2a/matchlogs/2023-2024/William-Saliba-Match-Logs",
#     "table_index": 0,
#     "header_row_index": 1,
#     "row_filters": [
#         {"column_name": "comp", "comparison": "!=", "value": "Premier League"}
#     ],
#     # "sub_table_config": {
#     #     "table_name": "fbref_team_players_standard",
#     #     "header_row_index": 1,
#     #     "hyperlink_data_stat": "team",
#     # },
# }
