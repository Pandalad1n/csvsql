import unittest
import psycopg2
import settings
from processor import Processor, TYPE_MAP
from datetime import datetime


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
        columns = (("biba", "int"), ("baba", "str"), ("buba", "datetime"))
        name = "database"
        proc = Processor(self.conn, name, columns, [])
        proc.create()
        with self.conn.cursor() as c:
            sql = """
            SELECT column_name, udt_name 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE table_name = '%s'
            """ % (name,)
            c.execute(sql)
            resp_columns = c.fetchall()
            self.assertEqual([(c[0], TYPE_MAP[c[1]].lower()) for c in columns], resp_columns)

    def test_adds_new_columns_if_not_exist(self):
        columns = (("biba", "int"), ("baba", "str"), ("buba", "datetime"))
        name = "database"
        proc = Processor(self.conn, name, columns, [])
        proc.create()

        columns = columns + (("new", "int"),)
        proc = Processor(self.conn, name, columns, [])
        proc.create()
        with self.conn.cursor() as c:
            sql = """
            SELECT column_name, udt_name 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE table_name = '%s'
            """ % (name,)
            c.execute(sql)
            resp_columns = c.fetchall()
            self.assertEqual([(c[0], TYPE_MAP[c[1]].lower()) for c in columns], resp_columns)

    def test_fills_data(self):
        columns = (("biba", "int"), ("baba", "str"), ("buba", "datetime"))
        name = "database"
        rows = ("111", "sss", "2016-06-22T19:10:25"), ("123", "asd", '2016-06-22T19:10:25')
        proc = Processor(self.conn, name, columns, rows)
        proc.create()
        proc.insert()
        with self.conn.cursor() as c:
            sql = """
            SELECT * 
            FROM %s
            """ % (name,)
            c.execute(sql)
            resp = c.fetchall()
            self.assertEqual([(int(r[0]), r[1], datetime.strptime(r[2], '%Y-%m-%dT%H:%M:%S')) for r in rows], resp)
