player_id_crosswalk = {
    "table_name": "player_id_crosswalk",
    "table_column_configs": [
        {
            "column_name": "fpl_player_id",
            "column_type": "VARCHAR (255)",
            "primary_key": True,
        },
        {
            "column_name": "fbref_player_id",
            "column_type": "VARCHAR (255)",
            "not_null": True,
        },
        {
            "column_name": "fpl_player_name",
            "column_type": "VARCHAR (255)",
            "not_null": True,
        },
        {
            "column_name": "fbref_player_name",
            "column_type": "VARCHAR (255)",
            "not_null": True,
        },
    ],
}
