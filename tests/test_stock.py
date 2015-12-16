import unittest
from datetime import datetime

from stock import Stock


class StockTest(unittest.TestCase):
    def test_new_stock_price(self):
        """A new stock should have a price that is None.
        """
        stock = Stock("GOOG")
        self.assertIsNone(stock.price)

    def test_stock_update(self):
        """An update should set the price on the stock object.

        Notes:
            We will be using the `datetime` module for the timestamp.
        """
        stock = Stock("GOOG")
        stock.update(datetime(2014, 2, 12), price=10)
        self.assertEqual(10, stock.price)

if __name__ == "__main__":
    unittest.main()
