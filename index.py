from fbref.configs.run_config import fbref_player_data_config
from fbref.configs.run_config import fbref_team_data_config
from run_scripts.create_schema_and_tables import create_schema_and_tables
from run_scripts.create_views import create_views
from run_scripts.generate_player_crosswalk import generate_player_crosswalk
from run_scripts.process_fbref_table import process_fbref_table
from run_scripts.process_fpl_api_data import process_fpl_api_data

SCHEMA_NAME = "test_schema"

CREATE_SCHEMA_AND_TABLES = True
PROCESS_FBREF_PLAYER_DATA = True
PROCESS_FBREF_TEAM_DATA = True
PROCESS_FPL_API_DATA = True
GENERATE_PLAYER_CROSSWALK = True
CREATE_PLAYER_VIEWS = True

if CREATE_SCHEMA_AND_TABLES:
    create_schema_and_tables(schema_name=SCHEMA_NAME)

if PROCESS_FBREF_PLAYER_DATA:
    process_fbref_table(
        schema_name=SCHEMA_NAME,
        table_url=fbref_player_data_config["table_url"],
        fbref_table_config=fbref_player_data_config,
    )

if PROCESS_FBREF_TEAM_DATA:
    process_fbref_table(
        schema_name=SCHEMA_NAME,
        table_url=fbref_team_data_config["table_url"],
        fbref_table_config=fbref_team_data_config,
    )

if PROCESS_FPL_API_DATA:
    process_fpl_api_data(schema_name=SCHEMA_NAME)

if GENERATE_PLAYER_CROSSWALK:
    generate_player_crosswalk(schema_name=SCHEMA_NAME)

if CREATE_PLAYER_VIEWS:
    create_views(schema_name=SCHEMA_NAME)
