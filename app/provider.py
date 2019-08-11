import csv
import openpyxl


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


class XlsxProvider:
    def __init__(self, xlsx_file):
        self.columns_cache = None
        self.rows_cache = None
        self.book = openpyxl.load_workbook(xlsx_file)

    def columns(self):
        if self.columns_cache:
            return self.columns_cache
        sheet = self.book.active
        self.columns_cache = tuple(v.value for v in next(sheet.rows))
        return self.columns_cache

    def rows(self):
        if self.rows_cache:
            return self.rows_cache
        sheet = self.book.active
        rows = sheet.rows
        next(rows)
        self.rows_cache = tuple(tuple(v.value for v in r) for r in rows)
        return self.rows_cache