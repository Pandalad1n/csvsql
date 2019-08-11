
class Processor:
    def __init__(self, connection, name, columns, rows):
        self.name = name
        self.rows = rows
        self.columns = columns
        self.connection = connection

    def create(self):

        sql = """
            CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});
        """.format(
            table_name=self.name,
            columns_sql=self.columns_types_sql(),
        )
        with self.connection.cursor() as c:
            c.execute(sql)

        sql = """
            SELECT column_name 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE table_name = '{}'
        """.format(self.name,)
        with self.connection.cursor() as c:
            c.execute(sql)
            db_columns = c.fetchall()
        for column in self.columns:
            if (column,) not in db_columns:
                sql = """
                    ALTER TABLE {table_name}
                    ADD COLUMN {column_sql} 
                """.format(
                    table_name=self.name,
                    column_sql=self.column_type_sql(column),
                )
                with self.connection.cursor() as c:
                    c.execute(sql)

    def insert(self):
        sql = """
            INSERT INTO {table_name} ({columns})
            VALUES {rows};
        """.format(
            table_name=self.name,
            columns=self.columns_sql(),
            rows=self.rows_sql(),
        )
        with self.connection.cursor() as c:
            c.execute(sql)

    def columns_types_sql(self):
        return ",".join([c + " VARCHAR" for c in self.columns])

    def column_type_sql(self, column):
        return column + " VARCHAR"

    def columns_sql(self):
        return ", ".join([c for c in self.columns])

    def rows_sql(self):
        return ", ".join(self.row_sql(r) for r in self.rows)

    def row_sql(self, row):
        return "(" + ", ".join("'" + c + "'" for c in row) + ")"
