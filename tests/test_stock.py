import unittest
from datetime import datetime

from stock import Stock, StockSignal


class StockTest(unittest.TestCase):
    def setUp(self):
        self.stock = Stock("GOOG")

    def test_price_of_new_stock_should_be_none(self):
        self.assertIsNone(self.stock.price)

    def test_stock_update_sets_correct_price(self):
        self.stock.update(datetime(2014, 2, 12), price=10)
        self.assertEqual(10, self.stock.price)

    def test_negative_price_should_throw_ValueError(self):
        self.assertRaises(ValueError, self.stock.update, datetime(2014, 2, 13), -10)

    def test_stock_price_should_return_latest_price(self):
        self.stock.update(datetime(2014, 2, 14), price=15.789)
        self.stock.update(datetime(2014, 2, 15), price=18.236458)
        self.stock.update(datetime(2014, 2, 16), price=23.12)
        self.assertAlmostEqual(23.12, self.stock.price, places=4)

    def test_price_is_the_latest_even_if_updates_are_made_out_of_order(self):
        self.stock.update(datetime(2014, 2, 10), price=10.2)
        self.stock.update(datetime(2014, 2, 15), price=15.789)
        self.stock.update(datetime(2014, 2, 11), price=18.236458)
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
        self.assertAlmostEquals(10.875, self.stock._closing_price(datetime(2014, 2, 14)), places=4)

    def test_date_closing_price_no_update(self):
        """Tests if the previous days closing price is returned if the date does not have an update.

        """
        self.assertAlmostEquals(10.72, self.stock._closing_price(datetime(2014, 2, 13)), places=4)

    def test_no_closing_prices_exception(self):
        """A stock without any closing prices should return an exception.

        """
        apple = Stock("AAPL")
        self.assertRaises(ValueError, apple._closing_price, datetime(2014, 2, 14))


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
        expected_moving_average = (12.281 + 10.875 + 10.72) / 3
        self.assertAlmostEquals(expected_moving_average, self.stock._moving_average(datetime(2014, 2, 15), 3), places=4)


class StockCrossoverSignalTest(unittest.TestCase):
    def setUp(self):
        self.stock = Stock("GOOG")
        timestamps = [
            datetime(2014, 5, 2, 10, 15), datetime(2014, 5, 2, 12, 15),
            datetime(2014, 5, 4, 12, 15),
            datetime(2014, 5, 5, 12, 15),
            datetime(2014, 5, 6, 10, 15), datetime(2014, 5, 6, 12, 15),
            datetime(2014, 5, 7, 14, 15),
            datetime(2014, 5, 8, 10, 15), datetime(2014, 5, 8, 12, 15), datetime(2014, 5, 8, 14, 15),
            datetime(2014, 5, 9, 12, 15), datetime(2014, 5, 9, 14, 15),
            datetime(2014, 5, 11, 10, 15), datetime(2014, 5, 11, 12, 15),
            datetime(2014, 5, 12, 14, 15),
            datetime(2014, 5, 13, 12, 15),
            datetime(2014, 5, 15, 14, 15),
            datetime(2014, 5, 17, 14, 15),
            datetime(2014, 5, 18, 14, 15),
            datetime(2014, 5, 19, 10, 15), datetime(2014, 5, 19, 12, 15), datetime(2014, 5, 19, 14, 15)
        ]
        prices = [
            48.726, 49.827,
            48.526,
            47.785,
            48.267, 47.023,
            46.956,
            44.821, 45.498, 46.423,
            47.125, 46.109,
            45.285, 44.234,
            45.068,
            47.237,
            48.715,
            46.234,
            45.238,
            44.526, 44.689, 44.856
        ]

        for timestamp, price in zip(timestamps, prices):
            self.stock.update(timestamp, price)

        self.assertAlmostEquals(44.856, self.stock.price, places=4)

    def test_short_term_upward_crossover_returns_buy_signal(self):

        self.assertEquals(StockSignal.buy, self.stock.get_cross_over_signal(datetime(2014, 5, 16)))

    def test_short_term_downward_crossover_returns_sell_signal(self):
        self.assertEquals(StockSignal.sell, self.stock.get_cross_over_signal(datetime(2014, 5, 20)))

    def test_no_crossover_returns_neutral_signal(self):
        self.assertEquals(StockSignal.neutral, self.stock.get_cross_over_signal(datetime(2014, 5, 14)))

    def test_insufficient_data_returns_neutral_stock_signal(self):
        self.assertEquals(StockSignal.neutral, self.stock.get_cross_over_signal(datetime(2014, 5, 9)))
