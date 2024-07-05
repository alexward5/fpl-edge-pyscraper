fbref_team_overall = {
    "table_name": "fbref_team_overall",
    "columns": [
        "team VARCHAR (255) PRIMARY KEY",
        "team_url VARCHAR (255) NOT NULL",
        "games INT NOT NULL",
        "wins INT NOT NULL",
        "ties INT NOT NULL",
        "losses INT NOT NULL",
        "goals_for INT NOT NULL",
        "goals_against INT NOT NULL",
        "goal_diff INT NOT NULL",
        "points INT NOT NULL",
        "points_avg DECIMAL NOT NULL",
        "xg_for DECIMAL NOT NULL",
        "xg_against DECIMAL NOT NULL",
        "xg_diff DECIMAL NOT NULL",
        "xg_diff_per90 DECIMAL NOT NULL",
        "attendance_per_g INT NOT NULL",
        "top_team_scorers VARCHAR (255) NOT NULL",
        "top_team_scorers_url VARCHAR (255) NOT NULL",
        "top_keeper VARCHAR (255) NOT NULL",
        "top_keeper_url VARCHAR (255) NOT NULL",
        "notes VARCHAR (255) NOT NULL",
    ],
}
