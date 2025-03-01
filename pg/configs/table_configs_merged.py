from typing import Any

from pg.configs.table_configs.fbref_player_matchlog import fbref_player_matchlog
from pg.configs.table_configs.fbref_team_overall import fbref_team_overall
from pg.configs.table_configs.fbref_team_players_standard import (
    fbref_team_players_standard,
)
from pg.configs.table_configs.fbref_team_scores_and_fixtures import (
    fbref_team_scores_and_fixtures,
)
from pg.configs.table_configs.fpl_player_data import fpl_player_data
from pg.configs.table_configs.player_id_crosswalk import player_id_crosswalk

table_configs_merged: dict[str, Any] = {
    "fbref_team_overall": fbref_team_overall,
    "fbref_team_players_standard": fbref_team_players_standard,
    "fbref_player_matchlog": fbref_player_matchlog,
    "fbref_team_scores_and_fixtures": fbref_team_scores_and_fixtures,
    "fpl_player_data": fpl_player_data,
    "player_id_crosswalk": player_id_crosswalk,
}
