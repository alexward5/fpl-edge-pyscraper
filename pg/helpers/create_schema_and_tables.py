from configs.table_configs_merged import table_configs_merged
from pg.helpers.build_column_sql import build_column_sql
from pg.PG import PG

pg = PG(dbname="postgres", user="postgres")


def create_schema_and_tables(schema_name: str):
    pg.drop_schema(schema_name)
    pg.create_schema(schema_name)

    for table_config in list(table_configs_merged.values()):
        pg.create_table(
            schema=schema_name,
            table_name=table_config["table_name"],
            columns=[
                build_column_sql(column_config)
                for column_config in table_config["table_column_configs"]
            ],
        )
