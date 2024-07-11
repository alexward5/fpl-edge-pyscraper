from typing import Any

import psycopg
from psycopg import sql


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
            print(f"Created schema: {schema_name}")

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
            print(f"Created table: {table_name}")

    def insert_row(
        self,
        schema: str,
        table_name: str,
        column_names: list[Any],
        row_values: list[Any],
    ):
        with self.conn.cursor() as cur:
            column_names_joined = ",".join(column_names)
            row_values_joined = ", ".join(f"'{val}'" for val in row_values)

            cur.execute(
                sql.SQL(
                    "INSERT INTO {schema}.{table_name}({column_names}) VALUES ({row_values}) ON CONFLICT DO NOTHING"
                ).format(
                    schema=sql.Identifier(schema),
                    table_name=sql.Identifier(table_name),
                    column_names=sql.SQL(column_names_joined),
                    row_values=sql.SQL(row_values_joined),  # type: ignore
                ),
            )

            self.conn.commit()
