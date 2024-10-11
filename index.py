from configs.run_config import fbref_table_config
from pg.helpers.create_schema_and_tables import create_schema_and_tables
from run_scripts.process_fbref_table import process_fbref_table

SCHEMA_NAME = "test_schema_new"

CREATE_SCHEMA_AND_TABLES = True
PROCESS_FBREF_TABLES = True

if CREATE_SCHEMA_AND_TABLES:
    create_schema_and_tables(schema_name=SCHEMA_NAME)

if PROCESS_FBREF_TABLES:
    process_fbref_table(
        schema_name=SCHEMA_NAME,
        table_url=fbref_table_config["table_url"],
        fbref_table_config=fbref_table_config,
    )
