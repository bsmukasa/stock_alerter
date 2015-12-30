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

    def test_increasing_trend_is_true_if_price_increases_for_3_updates(self):
        prices = [8, 10, 12]
        self.given_a_series_of_prices(prices)
        self.assertTrue(self.stock.is_increasing_trend)

    def test_increasing_trend_is_false_if_price_does_not_increase_for_3_updates(self):
        prices = [10, 8, 12]
        self.given_a_series_of_prices(prices)
        self.assertFalse(self.stock.is_increasing_trend)

    def test_increasing_trend_is_false_if_2_of_3_prices_are_equal(self):
        prices = [8, 10, 10]
        self.given_a_series_of_prices(prices)
        self.assertFalse(self.stock.is_increasing_trend)


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

    def test_correct_closing_price_is_returned_for_a_given_date(self):
        self.assertAlmostEquals(46.423, self.stock._closing_price(datetime(2014, 5, 8)), places=4)

    def test_previous_date_closing_price_is_returned_if_given_date_does_not_have_update(self):
        self.assertAlmostEquals(46.109, self.stock._closing_price(datetime(2014, 5, 10)), places=4)

    def test_stock_without_any_closing_prices_should_throw_ValueError(self):
        apple = Stock("AAPL")
        self.assertRaises(ValueError, apple._closing_price, datetime(2014, 2, 14))

    def test_calculation_of_three_day_moving_average(self):
        expected_moving_average = (46.234 + 48.715 + 48.715) / 3
        self.assertAlmostEquals(expected_moving_average, self.stock._moving_average(datetime(2014, 5, 17), 3), places=4)

    def test_short_term_upward_crossover_returns_buy_signal(self):
        self.assertEquals(StockSignal.buy, self.stock.get_cross_over_signal(datetime(2014, 5, 16)))

    def test_short_term_downward_crossover_returns_sell_signal(self):
        self.assertEquals(StockSignal.sell, self.stock.get_cross_over_signal(datetime(2014, 5, 20)))

    def test_no_crossover_returns_neutral_signal(self):
        self.assertEquals(StockSignal.neutral, self.stock.get_cross_over_signal(datetime(2014, 5, 14)))

    def test_insufficient_data_returns_neutral_stock_signal(self):
        self.assertEquals(StockSignal.neutral, self.stock.get_cross_over_signal(datetime(2014, 5, 9)))
