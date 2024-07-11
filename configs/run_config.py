from typing import Any


run_configs: list[dict[str, Any]] = [
    {
        "schema_name": "test_schema",
        "table_configs": [
            {
                "table_name": "fbref_team_overall",
                "table_url": "https://fbref.com/en/comps/9/Premier-League-Stats",
                "header_row_index": 0,
            }
        ],
    }
]
