import random
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
        self.assertTrue(self.stock.is_increasing_trend)

    def test_increasing_trend_false_3_updates_descending_prices(self):
        """Tests if prices from last three updates return as not increasing if they are descending.

        Use 3 updates.
        """
        prices = [10, 8, 12]
        self.given_a_series_of_prices(prices)
        self.assertFalse(self.stock.is_increasing_trend)

    def test_increasing_trend_false_3_updates_equal_prices(self):
        """Tests if prices from last three updates return as not increasing if two are equal.

        Use 3 updates.
        """
        prices = [8, 10, 10]
        self.given_a_series_of_prices(prices)
        self.assertFalse(self.stock.is_increasing_trend)

    def test_increasing_trend_true_tested_using_timestamps(self):
        """Tests if increasing trend is determined using timestamps is True as expected.

        Use 5 updates.
        """
        self.stock.update(datetime(2014, 2, 10), price=10)
        self.stock.update(datetime(2014, 2, 11), price=15.789)
        self.stock.update(datetime(2014, 2, 15), price=23.12)
        self.stock.update(datetime(2014, 2, 12), price=18.236458)
        self.stock.update(datetime(2014, 2, 9), price=10.2)
        self.assertTrue(self.stock.is_increasing_trend)

    def test_increasing_trend_false_tested_using_timestamps(self):
        """Tests if increasing trend is determined using timestamps is False as expected.

        Use 5 updates.
        """
        self.stock.update(datetime(2014, 2, 12), price=10)
        self.stock.update(datetime(2014, 2, 10), price=10.2)
        self.stock.update(datetime(2014, 2, 15), price=15.789)
        self.stock.update(datetime(2014, 2, 11), price=18.236458)
        self.stock.update(datetime(2014, 2, 9), price=23.12)
        self.assertFalse(self.stock.is_increasing_trend)


class StockClosingPriceTest(unittest.TestCase):
    def setUp(self):
        self.stock = Stock("GOOG")
        timestamps = [
            datetime(2014, 2, 11, 10, 15), datetime(2014, 2, 11, 12, 15), datetime(2014, 2, 11, 14, 15),
            datetime(2014, 2, 12, 8, 10), datetime(2014, 2, 12, 9, 15), datetime(2014, 2, 12, 10, 25),
            datetime(2014, 2, 12, 12, 30), datetime(2014, 2, 12, 14),
            datetime(2014, 2, 14, 9, 15), datetime(2014, 2, 14, 9, 45), datetime(2014, 2, 14, 10, 15),
            datetime(2014, 2, 14, 11, 25),
            datetime(2014, 2, 15, 12, 15), datetime(2014, 2, 15, 13, 15)
        ]
        prices = [
            10, 10.2, 10.789,
            11.2, 11.252, 11.123, 10.438, 10.72,
            10.382, 10.485, 10.628, 10.875,
            11.023, 12.281
        ]

        for timestamp, price in zip(timestamps, prices):
            self.stock.update(timestamp, price)

        self.assertAlmostEquals(12.281, self.stock.price, places=4)

    def test_date_closing_price(self):
        """Tests if closing price method returns the closing price for a given date.

        """
        self.assertAlmostEquals(10.875, self.stock.closing_price(datetime(2014, 2, 14)), places=4)

    def test_date_closing_price_no_update(self):
        """Tests if the previous days closing price is returned if the date does not have an update.

        """
        self.assertAlmostEquals(10.72, self.stock.closing_price(datetime(2014, 2, 13)), places=4)

    def test_no_closing_prices_exception(self):
        """A stock without any closing prices should return an exception.

        """
        apple = Stock("AAPL")
        self.assertRaises(ValueError, apple.closing_price, datetime(2014, 2, 14))


class StockMovingAverageTest(unittest.TestCase):
    def setUp(self):
        self.stock = Stock("GOOG")
        timestamps = [
            datetime(2014, 2, 11, 10, 15), datetime(2014, 2, 11, 12, 15), datetime(2014, 2, 11, 14, 15),
            datetime(2014, 2, 12, 8, 10), datetime(2014, 2, 12, 9, 15), datetime(2014, 2, 12, 10, 25),
            datetime(2014, 2, 12, 12, 30), datetime(2014, 2, 12, 14),
            datetime(2014, 2, 14, 9, 15), datetime(2014, 2, 14, 9, 45), datetime(2014, 2, 14, 10, 15),
            datetime(2014, 2, 14, 11, 25),
            datetime(2014, 2, 15, 12, 15), datetime(2014, 2, 15, 13, 15)
        ]
        prices = [
            10, 10.2, 10.789,
            11.2, 11.252, 11.123, 10.438, 10.72,
            10.382, 10.485, 10.628, 10.875,
            11.023, 12.281
        ]

        for timestamp, price in zip(timestamps, prices):
            self.stock.update(timestamp, price)

        self.assertAlmostEquals(12.281, self.stock.price, places=4)

    def test_three_day_moving_average(self):
        """Tests if the moving average for the previous three days.

        Moving average is the average of the closing prices for the previous three days.

        """
        self.fail()

    def test_insufficient_data_moving_average(self):
        """Tests if 0 is returned if there are not enough days to calculate a moving average.

        Use 10 days.

        """
        self.fail()
