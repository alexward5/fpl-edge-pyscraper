from configs.run_config import fbref_table_config
from utils.create_schema_and_tables import create_schema_and_tables
from utils.fbref_table_to_df import fbref_table_to_df

SCHEMA_NAME = "test_schema"
CREATE_SCHEMA_AND_TABLES = False

if CREATE_SCHEMA_AND_TABLES:
    create_schema_and_tables(schema_name=SCHEMA_NAME)

fbref_table_to_df(
    table_url=fbref_table_config["table_url"], fbref_table_config=fbref_table_config
)
