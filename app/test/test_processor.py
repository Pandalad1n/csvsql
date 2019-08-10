import unittest
import psycopg2
import settings
from processor import Processor


class TestDB(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDB, self).__init__(*args, **kwargs)

        self._initial_conn = psycopg2.connect(**settings.DB_CONFIG)
        self._initial_conn.autocommit = True
        self.conn = None

    def setUp(self):
        with self._initial_conn.cursor() as c:
            c.execute("DROP DATABASE IF EXISTS {}".format(settings.TEST_DB_CONFIG['dbname']))
            c.execute("CREATE DATABASE {}".format(settings.TEST_DB_CONFIG['dbname']))
        self.conn = psycopg2.connect(**settings.TEST_DB_CONFIG)

    def tearDown(self):
        self.conn.close()
        with self._initial_conn.cursor() as c:
            c.execute("DROP DATABASE {}".format(settings.TEST_DB_CONFIG['dbname']))

    def test_connection(self):
        with self.conn.cursor() as c:
            c.execute("SELECT 1")

    def test_creates_table(self):
        columns = ("banme", "mane", "lmene")
        name = "bibia"
        proc = Processor(self.conn, name, columns, [])
        proc.create()
        with self.conn.cursor() as c:
            c.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}'".format(name))
            resp_columns = c.fetchall()
            self.assertEqual([(c,) for c in columns], resp_columns)

    def test_fills_data(self):
        columns = ("banme", "mane", "lmene")
        name = "bibia"
        rows = ("bobo1", "baba1", "bebe1"), ("bobo2", "baba2", "bebe2"), ("bobo3", "baba3", "bebe3")
        proc = Processor(self.conn, name, columns, rows)
        proc.create()
        proc.insert()
        with self.conn.cursor() as c:
            c.execute("SELECT * FROM {}".format(name))
            resp = c.fetchall()
            self.assertEqual([r for r in rows], resp)
