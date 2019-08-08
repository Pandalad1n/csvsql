import unittest
import psycopg2


class TestDB(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDB, self).__init__(*args, **kwargs)

        self._initial_conn = psycopg2.connect("user=postgres host=db password=1234 port=5432")
        self._initial_conn.autocommit = True
        self.conn = None

    def setUp(self):
        with self._initial_conn.cursor() as c:
            c.execute("CREATE DATABASE test")
        self.conn = psycopg2.connect("dbname=test user=postgres host=db password=1234 port=5432")

    def tearDown(self):
        self.conn.close()
        with self._initial_conn.cursor() as c:
            c.execute("DROP DATABASE test")

    def test_connection(self):
        with self.conn.cursor() as c:
            c.execute("SELECT 1")


if __name__ == '__main__':
    unittest.main()
