
class Processor:
    def __init__(self, connection, name, columns, rows):
        self.name = name
        self.rows = rows
        self.columns = columns
        self.connection = connection

    def process(self):
        with self.connection.cursor() as c:
            c.execute("""
                CREATE TABLE {table_name} ({columns_sql});
            """.format(
                table_name=self.name,
                columns_sql=self.columns_sql(),
            ))

    def columns_sql(self):
        return ",".join([c + " VARCHAR" for c in self.columns])
