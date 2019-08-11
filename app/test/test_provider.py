from provider import CSVProvider, XlsxProvider
import unittest
import io
from openpyxl import Workbook

class TestCSVProvider(unittest.TestCase):
    def test_data(self):
        csv_file = io.StringIO(
"""biba,baba,buba
ttt,111,2222
sss,333,4444
""")
        prov = CSVProvider(csv_file)
        self.assertEqual(("biba", "baba", "buba"), prov.columns())
        self.assertEqual((("ttt", "111", "2222"), ("sss", "333", "4444")), prov.rows())


class TestXlsxProvider(unittest.TestCase):
    def test_data(self):

        book = Workbook()
        sheet = book.active
        file = io.BytesIO()

        sheet.append(['biba', 'baba', 'buba'])
        sheet.append(['This is A2', 'This is B2', 'This is C2'])
        sheet.append(['This is A3', 'This is B3', 'This is C3'])

        book.save(file)

        prov = XlsxProvider(file)
        self.assertEqual(("biba", "baba", "buba"), prov.columns())
        self.assertEqual((('This is A2', 'This is B2', 'This is C2'), ('This is A3', 'This is B3', 'This is C3')), prov.rows())
