from typing import Any

run_config: dict[str, Any] = {
    "table_name": "fbref_team_overall",
    "table_url": "https://fbref.com/en/comps/9/Premier-League-Stats",
    "header_row_index": 0,
    "sub_table_config": {
        "table_name": "fbref_team_players_standard",
        "header_row_index": 1,
        "hyperlink_data_stat": "team",
    },
}
