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


PG("postgres", "postgres").create_schema("best_table_na")
