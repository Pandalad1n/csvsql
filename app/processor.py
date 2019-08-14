TYPE_MAP = {
    "str": "VARCHAR",
    "int": "INT4",
    "datetime": "TIMESTAMP",
}


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
        """.format(self.name)
        with self.connection.cursor() as c:
            c.execute(sql)
            db_columns = {c[0] for c in c.fetchall()}
        new_columns = tuple(c for c in self.columns if c[0] not in db_columns)
        if not new_columns:
            return
        sql = """
            ALTER TABLE {table_name}
            {columns_sql} 
        """.format(
            table_name=self.name,
            columns_sql=self.add_columns_sql(new_columns),
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
        return ",".join([self.column_type_sql(c) for c in self.columns])

    def add_columns_sql(self, columns):
        return ",".join(["ADD COLUMN " + self.column_type_sql(c) for c in columns])

    def column_type_sql(self, column):
        return column[0] + " " + TYPE_MAP[column[1]]

    def columns_sql(self):
        return ", ".join([c[0] for c in self.columns])

    def rows_sql(self):
        return ", ".join(self.row_sql(r) for r in self.rows)

    def row_sql(self, row):
        return "(" + ", ".join("'" + c + "'" for c in row) + ")"
