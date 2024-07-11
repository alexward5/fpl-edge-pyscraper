from typing import Any

from configs.table_configs.fbref_team_overall import fbref_team_overall
from configs.table_configs.fbref_team_standard import fbref_team_standard

merged_table_configs: dict[str, Any] = {
    "fbref_team_overall": fbref_team_overall,
    "fbref_team_standard": fbref_team_standard,
}
