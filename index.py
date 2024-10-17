from configs.run_config import fbref_table_config
from run_scripts.create_schema_and_tables import create_schema_and_tables
from run_scripts.process_fbref_table import process_fbref_table
from run_scripts.process_fpl_api_data import process_fpl_api_data

SCHEMA_NAME = "test_schema_new"

CREATE_SCHEMA_AND_TABLES = True
PROCESS_FBREF_TABLES = True
PROCESS_FPL_API_DATA = True

if CREATE_SCHEMA_AND_TABLES:
    create_schema_and_tables(schema_name=SCHEMA_NAME)

if PROCESS_FBREF_TABLES:
    process_fbref_table(
        schema_name=SCHEMA_NAME,
        table_url=fbref_table_config["table_url"],
        fbref_table_config=fbref_table_config,
    )

if PROCESS_FPL_API_DATA:
    process_fpl_api_data()
