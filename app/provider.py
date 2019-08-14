import csv
import openpyxl
from datetime import datetime


class CSVProvider:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.columns_cache = None
        self.rows_cache = None

    def columns(self):
        if self.columns_cache:
            return self.columns_cache
        reader = csv.reader(self.csv_file)
        column_names = tuple(next(reader, None))
        row = tuple(next(reader, None))
        result = []
        for i, name in enumerate(column_names):
            result.append((name, detect_type(row[i])))
        self.columns_cache = tuple(result)
        return self.columns_cache

    def rows(self):
        self.columns()
        if self.rows_cache:
            return self.rows_cache
        self.csv_file.seek(0)
        reader = csv.reader(self.csv_file)
        next(reader, None)
        self.rows_cache = tuple(tuple(convert_type(r) for r in row) for row in reader)
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


def detect_type(value):
    try:
        int(value)
        return "int"
    except ValueError:
        pass

    try:
        datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        return "datetime"
    except (TypeError, ValueError):
        pass

    return "str"


def convert_type(value):
    try:
        return int(value)
    except ValueError:
        pass

    try:
        return int(datetime.strptime(value, '%Y-%m-%dT%H:%M:%S').timestamp())
    except (TypeError, ValueError):
        pass

    return value
