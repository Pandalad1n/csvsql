from psycopg2 import sql as sql_format

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
            CREATE TABLE IF NOT EXISTS {} ({});
        """.format('{}', ','.join('{} ' + TYPE_MAP[c[1]] for c in self.columns))
        query = sql_format.SQL(sql)
        with self.connection.cursor() as c:
            c.execute(query.format(sql_format.Identifier(self.name), *[sql_format.Identifier(c[0]) for c in self.columns]))

        sql = """
            SELECT column_name
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE table_name = {}
        """
        query = sql_format.SQL(sql)
        with self.connection.cursor() as c:
            c.execute(query.format(sql_format.Literal(self.name)))
            db_columns = {c[0] for c in c.fetchall()}
        new_columns = tuple(c for c in self.columns if c[0] not in db_columns)
        if not new_columns:
            return
        sql = """
            ALTER TABLE {{}}
            {}
        """.format(",".join("ADD COLUMN {} " + TYPE_MAP[c[1]] for c in new_columns))
        query = sql_format.SQL(sql)
        with self.connection.cursor() as c:
            c.execute(query.format(sql_format.Identifier(self.name), *[sql_format.Identifier(c[0]) for c in new_columns]))

    def insert(self):
        rows = []
        for row in self.rows:
            vals = ["{}" for _ in row]
            rows.append('(' + ",".join(vals) + ')')
        val_template = ",".join(rows)

        vals = []
        for row in self.rows:
            for val in row:
                vals.append(sql_format.Literal(val))

        sql = """
            INSERT INTO {{}} ({})
            VALUES {};
        """.format(",".join("{}" for _ in self.columns), val_template)
        query = sql_format.SQL(sql)

        with self.connection.cursor() as c:
            c.execute(query.format(
                sql_format.Identifier(self.name),
                *[sql_format.Identifier(c[0]) for c in self.columns],
                *vals,
            ))

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
