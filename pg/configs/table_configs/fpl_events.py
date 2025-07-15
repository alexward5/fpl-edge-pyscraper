from typing import Any

fpl_events: dict[str, Any] = {
    "table_name": "fpl_events",
    "table_column_configs": [
        {"column_name": "id", "column_type": "INT", "primary_key": True},
        {"column_name": "name", "column_type": "VARCHAR(255)", "not_null": True},
        {
            "column_name": "deadline_time",
            "column_type": "VARCHAR(255)",
            "not_null": True,
        },
        {
            "column_name": "release_time",
            "column_type": "VARCHAR(255)",
            "not_null": False,
        },
        {"column_name": "average_entry_score", "column_type": "INT", "not_null": True},
        {"column_name": "finished", "column_type": "BOOLEAN", "not_null": True},
        {"column_name": "data_checked", "column_type": "BOOLEAN", "not_null": True},
        {
            "column_name": "highest_scoring_entry",
            "column_type": "INT",
            "not_null": True,
        },
        {
            "column_name": "deadline_time_epoch",
            "column_type": "BIGINT",
            "not_null": True,
        },
        {
            "column_name": "deadline_time_game_offset",
            "column_type": "INT",
            "not_null": True,
        },
        {"column_name": "highest_score", "column_type": "INT", "not_null": True},
        {"column_name": "is_previous", "column_type": "BOOLEAN", "not_null": True},
        {"column_name": "is_current", "column_type": "BOOLEAN", "not_null": True},
        {"column_name": "is_next", "column_type": "BOOLEAN", "not_null": True},
        {
            "column_name": "cup_leagues_created",
            "column_type": "BOOLEAN",
            "not_null": True,
        },
        {
            "column_name": "h2h_ko_matches_created",
            "column_type": "BOOLEAN",
            "not_null": True,
        },
        {"column_name": "can_enter", "column_type": "BOOLEAN", "not_null": True},
        {"column_name": "can_manage", "column_type": "BOOLEAN", "not_null": True},
        {"column_name": "released", "column_type": "BOOLEAN", "not_null": True},
        {"column_name": "ranked_count", "column_type": "INT", "not_null": True},
        {"column_name": "most_selected", "column_type": "INT", "not_null": True},
        {"column_name": "most_transferred_in", "column_type": "INT", "not_null": True},
        {"column_name": "top_element", "column_type": "INT", "not_null": True},
        {"column_name": "transfers_made", "column_type": "INT", "not_null": True},
        {"column_name": "most_captained", "column_type": "INT", "not_null": True},
        {"column_name": "most_vice_captained", "column_type": "INT", "not_null": True},
    ],
}
