from configs.table_configs_merged import table_configs_merged
from pg.PG import PG
from utils.build_column_sql import build_column_sql

pg = PG(dbname="postgres", user="postgres")

SCHEMA_NAME = "test_schema"

pg.drop_schema(schema_name=SCHEMA_NAME)


def create_schema_and_tables():
    pg.create_schema(schema_name=SCHEMA_NAME)

    for table_config in list(table_configs_merged.values()):
        pg.create_table(
            schema=SCHEMA_NAME,
            table_name=table_config["table_name"],
            columns=[
                build_column_sql(column_config)
                for column_config in table_config["table_column_configs"]
            ],
        )
