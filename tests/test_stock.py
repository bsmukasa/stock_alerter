import unittest
from datetime import datetime

from stock import Stock


class StockTest(unittest.TestCase):
    def setUp(self):
        self.stock = Stock("GOOG")

    def test_new_stock_price(self):
        """A new stock should have a price that is None.

        """
        self.assertIsNone(self.stock.price)

    def test_stock_update(self):
        """An update should set the price on the stock object.

        Notes:
            We will be using the `datetime` module for the timestamp.
        """
        self.stock.update(datetime(2014, 2, 12), price=10)
        self.assertEqual(10, self.stock.price)

    def test_negative_price_exception(self):
        """An update with a negative price should return a value error.

        """
        self.assertRaises(ValueError, self.stock.update, datetime(2014, 2, 13), -10)

    def test_stock_holds_latest_price(self):
        """A stock should hold the latest price.

        Executes five updates.
        """
        self.stock.update(datetime(2014, 2, 12), price=10)
        self.stock.update(datetime(2014, 2, 12), price=10.2)
        self.stock.update(datetime(2014, 2, 12), price=15.789)
        self.stock.update(datetime(2014, 2, 12), price=18.236458)
        self.stock.update(datetime(2014, 2, 12), price=23.12)
        self.assertAlmostEqual(23.12, self.stock.price, places=4)

    def test_stock_returns_latest_timestamp_price(self):
        """A stock should return the latest price per timestamp.

        """
        self.stock.update(datetime(2014, 2, 12), price=10)
        self.stock.update(datetime(2014, 2, 10), price=10.2)
        self.stock.update(datetime(2014, 2, 15), price=15.789)
        self.stock.update(datetime(2014, 2, 11), price=18.236458)
        self.stock.update(datetime(2014, 2, 9), price=23.12)
        self.assertAlmostEqual(15.789, self.stock.price, places=4)
