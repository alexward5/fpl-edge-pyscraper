fbref_team_overall = {
    "table_name": "fbref_team_overall",
    "table_column_configs": [
        {
            "column_name": "rank",
            "column_type": "INT",
            "primary_key": True,
        },
        {
            "column_name": "team",
            "column_type": "VARCHAR (255)",
            "not_null": True,
        },
        {
            "column_name": "games",
            "column_type": "INT",
            "not_null": True,
        },
        {
            "column_name": "wins",
            "column_type": "INT",
            "not_null": True,
        },
        {
            "column_name": "ties",
            "column_type": "INT",
            "not_null": True,
        },
        {
            "column_name": "losses",
            "column_type": "INT",
            "not_null": True,
        },
        {
            "column_name": "goals_for",
            "column_type": "INT",
            "not_null": True,
        },
        {
            "column_name": "goals_against",
            "column_type": "INT",
            "not_null": True,
        },
        {
            "column_name": "goal_diff",
            "column_type": "INT",
            "not_null": True,
        },
        {
            "column_name": "points",
            "column_type": "INT",
            "not_null": True,
        },
        {
            "column_name": "points_avg",
            "column_type": "DECIMAL",
            "not_null": True,
        },
        {
            "column_name": "xg_for",
            "column_type": "DECIMAL",
            "not_null": True,
        },
        {
            "column_name": "xg_against",
            "column_type": "DECIMAL",
            "not_null": True,
        },
        {
            "column_name": "xg_diff",
            "column_type": "DECIMAL",
            "not_null": True,
        },
        {
            "column_name": "xg_diff_per90",
            "column_type": "DECIMAL",
            "not_null": True,
        },
        {
            "column_name": "attendance_per_g",
            "column_type": "INT",
            "not_null": True,
        },
        {
            "column_name": "top_team_scorers",
            "column_type": "VARCHAR (255)",
            "not_null": True,
        },
        {
            "column_name": "top_keeper",
            "column_type": "VARCHAR (255)",
            "not_null": True,
        },
        {
            "column_name": "notes",
            "column_type": "VARCHAR (255)",
            "not_null": True,
        },
    ],
}
