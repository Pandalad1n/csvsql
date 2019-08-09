import csv


class CSVProvider:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.columns_cache = None
        self.rows_cache = None

    def columns(self):
        if self.columns_cache:
            return self.columns_cache
        reader = csv.reader(self.csv_file)
        self.columns_cache = tuple(next(reader, None))
        return self.columns_cache

    def rows(self):
        self.columns()
        if self.rows_cache:
            return self.rows_cache
        reader = csv.reader(self.csv_file)
        self.rows_cache = tuple(tuple(row) for row in reader)
        return self.rows_cache
