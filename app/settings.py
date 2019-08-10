import os


DEBUG = True

DB_CONFIG = {
    'user': os.environ['PGUSER'],
    'host': os.environ['PGHOST'],
    'password': os.environ['PGPASSWORD'],
    'port': os.environ['PGPORT'],
    'dbname': os.environ['PGDATABASE'],
}
TEST_DB_CONFIG = {
    'user': os.environ['PGUSER'],
    'host': os.environ['PGHOST'],
    'password': os.environ['PGPASSWORD'],
    'port': os.environ['PGPORT'],
    'dbname': os.environ['PGDATABASE'] + "_test",
}

