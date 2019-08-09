from provider import CSVProvider
import unittest
import io



class TestProvider(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestProvider, self).__init__(*args, **kwargs)

    def test_data(self):
        csv_file = io.StringIO(
"""biba,baba,buba
ttt,111,2222
sss,333,4444
""")
        prov = CSVProvider(csv_file)
        self.assertEqual(("biba", "baba", "buba"), prov.columns())
        self.assertEqual((("ttt", "111", "2222"), ("sss", "333", "4444")), prov.rows())
