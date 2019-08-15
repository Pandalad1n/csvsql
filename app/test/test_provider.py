from provider import CSVProvider, XlsxProvider
import unittest
import io
from openpyxl import Workbook
import csv
from datetime import datetime


class TestCSVProvider(unittest.TestCase):
    def test_data(self):
        csv_file = io.StringIO()
        writer = csv.writer(csv_file)
        writer.writerow(['biba', 'baba', 'buba'])
        writer.writerow([111, 'sss', datetime(2016, 6, 22, 19, 10, 25).isoformat()])
        writer.writerow([123, 'baba', datetime(2012, 6, 22, 11, 10, 28).isoformat()])
        csv_file.seek(0)

        prov = CSVProvider(csv_file)
        self.assertEqual((("biba", "int"), ("baba", "str"), ("buba", "datetime")), prov.columns())
        self.assertEqual(((111, "sss", datetime(2016, 6, 22, 19, 10, 25)), (123, "baba", datetime(2012, 6, 22, 11, 10, 28))), prov.rows())


class TestXlsxProvider(unittest.TestCase):
    def test_data(self):

        book = Workbook()
        sheet = book.active
        file = io.BytesIO()

        sheet.append(['biba', 'baba', 'buba'])
        sheet.append([111, 'sss', datetime(2016, 6, 22, 19, 10, 25).isoformat()])
        sheet.append([123, 'baba', datetime(2012, 6, 22, 11, 10, 28).isoformat()])

        book.save(file)

        prov = XlsxProvider(file)
        self.assertEqual((("biba", "int"), ("baba", "str"), ("buba", "datetime")), prov.columns())
        self.assertEqual(((111, "sss", datetime(2016, 6, 22, 19, 10, 25)), (123, "baba", datetime(2012, 6, 22, 11, 10, 28))), prov.rows())
