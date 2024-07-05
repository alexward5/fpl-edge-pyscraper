import psycopg
from psycopg import sql
from typing import Any


class PG:
    def __init__(self, dbname: str, user: str):
        self.conn = psycopg.connect(f"dbname={dbname} user={user}")

    def __del__(self):
        self.conn.close()

    def create_schema(self, schema_name: str):
        with self.conn.cursor() as cur:
            cur.execute(
                sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(
                    sql.Identifier(schema_name)
                ),
            )

            self.conn.commit()

    def create_table(self, schema: str, table_name: str, columns: list[Any]):
        with self.conn.cursor() as cur:
            cur.execute(
                sql.SQL(
                    "CREATE TABLE IF NOT EXISTS {schema}.{table_name} ({columns})"
                ).format(
                    schema=sql.Identifier(schema),
                    table_name=sql.Identifier(table_name),
                    columns=sql.SQL(",".join(columns)),
                ),
            )

            self.conn.commit()


SCHEMA_NAME = "TEST_SCHEMA"
TABLE_NAME = "TEST_TABLE"


PG("postgres", "postgres").create_schema(SCHEMA_NAME)
PG("postgres", "postgres").create_table(
    SCHEMA_NAME,
    TABLE_NAME,
    [
        "user_id SERIAL PRIMARY KEY",
        "username VARCHAR (50) UNIQUE NOT NULL",
    ],
)
