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


class StockTrendTest(unittest.TestCase):
    def setUp(self):
        self.stock = Stock("GOOG")

    def given_a_series_of_prices(self, prices):
        """Executes an update for each of three given prices.

        Args:
            prices: The price list.
        """
        timestamps = [datetime(2014, 2, 11), datetime(2014, 2, 12), datetime(2014, 2, 13)]
        for timestamp, price in zip(timestamps, prices):
            self.stock.update(timestamp, price)

    def test_increasing_trend_true_3_updates(self):
        """Tests if prices from last three updates return as increasing if they are ascending.

        Use 3 updates.
        """
        prices = [8, 10, 12]
        self.given_a_series_of_prices(prices)
        self.assertTrue(self.stock.is_increasing_trend())

    def test_increasing_trend_false_3_updates_descending_prices(self):
        """Tests if prices from last three updates return as not increasing if they are descending.

        Use 3 updates.
        """
        prices = [10, 8, 12]
        self.given_a_series_of_prices(prices)
        self.assertFalse(self.stock.is_increasing_trend())

    def test_increasing_trend_false_3_updates_equal_prices(self):
        """Tests if prices from last three updates return as not increasing if two are equal.

        Use 3 updates.
        """
        prices = [8, 10, 10]
        self.given_a_series_of_prices(prices)
        self.assertFalse(self.stock.is_increasing_trend())


if __name__ == "__main__":
    unittest.main()
