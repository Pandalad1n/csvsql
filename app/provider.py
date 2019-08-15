import csv
import openpyxl
from datetime import datetime


class CSVProvider:
    def __init__(self, csv_file):
        """
        :param csv_file: File descriptor to read from.
        """
        self.csv_file = csv_file
        self.columns_cache = None
        self.rows_cache = None

    def columns(self):
        """
        :return column names with types
        """
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
        """
        :return rows and converts types
        """
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
        """
        :param xlsx_file: File descriptor to read from.
        """
        self.columns_cache = None
        self.rows_cache = None
        self.book = openpyxl.load_workbook(xlsx_file)

    def columns(self):
        """
        :return column names with types
        """
        if self.columns_cache:
            return self.columns_cache
        sheet = self.book.active
        rows = sheet.rows
        column_names = tuple(next(rows, None))
        row = tuple(next(rows, None))
        result = []
        for i, name in enumerate(column_names):
            result.append((name.value, detect_type(row[i].value)))
        self.columns_cache = tuple(result)
        return self.columns_cache

    def rows(self):
        """
        :return rows and converts types
        """
        if self.rows_cache:
            return self.rows_cache
        sheet = self.book.active
        rows = sheet.rows
        next(rows)
        self.rows_cache = tuple(tuple(convert_type(v.value) for v in r) for r in rows)
        return self.rows_cache


def detect_type(value):
    try:
        int(value)
        return "int"
    except ValueError:
        pass

    try:
        datetime.fromisoformat(value)
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
        return datetime.fromisoformat(value)
    except (TypeError, ValueError):
        pass

    return value
