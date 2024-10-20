from typing import Any

from pg.configs.table_configs.fbref_player_matchlog import fbref_player_matchlog
from pg.configs.table_configs.fbref_team_overall import fbref_team_overall
from pg.configs.table_configs.fbref_team_players_standard import (
    fbref_team_players_standard,
)
from pg.configs.table_configs.fpl_player_data import fpl_player_data

table_configs_merged: dict[str, Any] = {
    "fbref_team_overall": fbref_team_overall,
    "fbref_team_players_standard": fbref_team_players_standard,
    "fbref_player_matchlog": fbref_player_matchlog,
    "fpl_player_data": fpl_player_data,
}
