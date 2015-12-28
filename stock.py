# -*- coding: utf-8 -*-
"""Stock class and associated features.

Attributes:
    stock_price_event: A namedtuple with timestamp and price of a stock price update.

"""
import bisect
import collections

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

        Returns: Most recent price.

        """
        return self.price_history[-1].price if self.price_history else None

    def update(self, timestamp, price):
        """Updates the stock's price history.

        Args:
            timestamp: The timestamp of the update.
            price: The new price of the stock.

        """
        if price < 0:
            raise ValueError("price should not be negative")
        bisect.insort_left(self.price_history, stock_price_event(timestamp, price))

    def is_increasing_trend(self):
        """Determines if last three prices were ascending in value.

        Returns: True if there is an increasing trend, False if not.

        """
        return self.price_history[-3].price < self.price_history[-2].price < self.price_history[-1].price
