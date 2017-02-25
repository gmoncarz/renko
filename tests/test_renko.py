import unittest
import pandas as pd

from renko import RenkoFixBrickSize

class RenkoFixBrickSizeTest(unittest.TestCase):
    def setUp(self):
        self._data = pd.DataFrame({
            'price': [20, 22, 25,
                      25.01, 26, 29, 30,
                      30.01, 33, 35,
                      36, 40,
                      42,
                      57, 58,
                      64, 65,
                      69,
                      62, 61, 65, 60,
                      56],
            'volume': [1, 2, 3,
                      4, 5, 6, 7,
                      8, 9, 10,
                      11, 12,
                      13,
                      14, 15,
                      16, 17,
                      18,
                      19, 20, 21, 22,
                      23],
        })
        pass

    def test_prices_without_volume_neither_dates(self):
        subject = RenkoFixBrickSize(5, 'test')
        subject.new_quotes(self._data.price[:].tolist())
        pass

    def test_prices_with_volume_but_not_dates(self):
        subject = RenkoFixBrickSize(5, 'test')
        subject.new_quotes(self._data.price[:].tolist(),
                           volumes=self._data.volume[:].tolist())
        import ipdb; ipdb.set_trace()
        pass
