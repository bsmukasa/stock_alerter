import bisect
import collections

PriceEvent = collections.namedtuple("PriceEvent", ["timestamp", "price"])


class Stock:
    def __init__(self, symbol):
        """Constructor for Stock instance.

        Args:
            symbol: The stock symbol.
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
        bisect.insort_left(self.price_history, PriceEvent(timestamp, price))
