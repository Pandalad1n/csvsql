from psycopg2 import sql as sql_format

TYPE_MAP = {
    "str": "VARCHAR",
    "int": "INT4",
    "datetime": "TIMESTAMP",
}


class Processor:
    def __init__(self, connection, name, columns, rows):
        """
        :param connection: Opened connection from postgres driver. Needs to be closed by client.
        :param name: Table name.
        :param columns: Table columns.
        :param rows: Table rows.
        """
        self.name = name
        self.rows = rows
        self.columns = columns
        self.connection = connection

    def create(self):
        """
        Creates table with provided columns.
        If table already exists adds new columns to the existing table.
        """
        # creating table if not exists
        sql = """
            CREATE TABLE IF NOT EXISTS {} ({});
        """.format('{}', ','.join('{} ' + TYPE_MAP[c[1]] for c in self.columns))
        query = sql_format.SQL(sql)
        with self.connection.cursor() as c:
            c.execute(query.format(sql_format.Identifier(self.name), *[sql_format.Identifier(c[0]) for c in self.columns]))
        # selecting all columns from existing table
        sql = """
            SELECT column_name
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE table_name = {}
        """
        query = sql_format.SQL(sql)
        with self.connection.cursor() as c:
            c.execute(query.format(sql_format.Literal(self.name)))
            db_columns = {c[0] for c in c.fetchall()}
        # filtering columns that do not exist in the table. If no new columns do nothing
        new_columns = tuple(c for c in self.columns if c[0] not in db_columns)
        if not new_columns:
            return
        # add new columns to the existing table
        sql = """
            ALTER TABLE {{}}
            {}
        """.format(",".join("ADD COLUMN {} " + TYPE_MAP[c[1]] for c in new_columns))
        query = sql_format.SQL(sql)
        with self.connection.cursor() as c:
            c.execute(query.format(sql_format.Identifier(self.name), *[sql_format.Identifier(c[0]) for c in new_columns]))

    def insert(self):
        """
        Inserts provided rows into the table.
        Returns error if table does not exists. Call `create` to create table.
        """
        # creating values template
        rows = []
        for row in self.rows:
            vals = ["{}" for _ in row]
            rows.append('(' + ",".join(vals) + ')')
        val_template = ",".join(rows)
        # creating value literals
        vals = []
        for row in self.rows:
            for val in row:
                vals.append(sql_format.Literal(val))
        # creating sql template
        sql = """
            INSERT INTO {{}} ({})
            VALUES {};
        """.format(",".join("{}" for _ in self.columns), val_template)
        query = sql_format.SQL(sql)
        # executing query
        with self.connection.cursor() as c:
            c.execute(query.format(
                sql_format.Identifier(self.name),
                *[sql_format.Identifier(c[0]) for c in self.columns],
                *vals,
            ))

