from configs.run_config import fbref_table_config
from pg.PG import PG
from utils.create_schema_and_tables import create_schema_and_tables
from utils.fbref_table_to_df import fbref_table_to_df

pg = PG(dbname="postgres", user="postgres")

SCHEMA_NAME = "test_schema"
CREATE_SCHEMA_AND_TABLES = True

if CREATE_SCHEMA_AND_TABLES:
    create_schema_and_tables(schema_name=SCHEMA_NAME)

fbref_table_df = fbref_table_to_df(
    table_url=fbref_table_config["table_url"], fbref_table_config=fbref_table_config
)

for index, row in fbref_table_df.iterrows():
    pg.insert_row(
        schema=SCHEMA_NAME,
        table_name=fbref_table_config["table_name"],
        column_names=fbref_table_df.columns.to_list(),
        row_values=row.to_list(),
    )
