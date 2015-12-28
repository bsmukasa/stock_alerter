# -*- coding: utf-8 -*-
"""Stock class and associated features.

Attributes:
    stock_price_event: A namedtuple with timestamp and price of a stock price update.

"""
import bisect
import collections

from datetime import timedelta

stock_price_event = collections.namedtuple("stock_price_event", ["timestamp", "price"])


class Stock:
    def __init__(self, symbol):
        """A Stock object representing its price history.

        Args:
            symbol (str): The stock symbol.

        Attributes:
            symbol (str): The stock symbol.
            price (float): The most recent price.

        """
        self.symbol = symbol
        self.price_history = []

    @property
    def price(self):
        """Returns the stocks most recent price.

        Returns:
            Most recent price.

        """
        return self.price_history[-1].price if self.price_history else None

    def update(self, timestamp, price):
        """Updates the stock's price history.

        Args:
            timestamp: The timestamp of the update.
            price: The new price of the stock.

        Raises:
            ValueError: If price is less than zero.

        """
        if price < 0:
            raise ValueError("price should not be negative")
        bisect.insort_left(self.price_history, stock_price_event(timestamp, price))

    @property
    def is_increasing_trend(self):
        """Determines if last three prices were ascending in value.

        Returns:
            True if there is an increasing trend, False if not.

        """
        return self.price_history[-3].price < self.price_history[-2].price < self.price_history[-1].price

    def closing_price(self, timestamp):
        """Returns a given dates closing price.

        This is the stock's last price from an update on the date or the closing price for the previous day if an
        update has not occurred.

        Args:
            timestamp: The timestamp being checked for a closing price.

        Raises:
            ValueError: If stock has not had any updates.

        Returns:
            Closing price if it exists, executes self.closing_price(previous day) if not.

        """
        if self.price_history:
            date_history = [
                stock_price_event for stock_price_event in self.price_history if stock_price_event.timestamp.date() ==
                timestamp.date()
                ]
            return date_history[-1].price if date_history else self.closing_price(timestamp - timedelta(days=1))
        else:
            raise ValueError("stock has not had any updates")

    def moving_average(self, timestamp, num_of_days):
        dates = [timestamp - timedelta(days=i) for i in range(num_of_days)]
        closing_prices = [self.closing_price(date) for date in dates]
        average_closing_price = sum(closing_prices) / num_of_days
        return average_closing_price
