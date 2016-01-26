from datetime import timedelta
from enum import Enum

from event import Event
from moving_average import MovingAverage
from timeseries import TimeSeries


class StockSignal(Enum):
    buy = 1
    neutral = 0
    sell = -1


class Stock:
    LONG_TERM_TIME_SPAN = 10
    SHORT_TERM_TIME_SPAN = 5

    def __init__(self, symbol):
        """A Stock object representing its price history.

        Args:
            symbol (str): The stock symbol.

        Attributes:
            symbol (str): The stock symbol.
            price (float): The most recent price.
            history (TimeSeries): The record of stock price updates by timestamp and price.
            update_event (Event): The event that is called when an update occurs to the stocks history.

        """
        self.symbol = symbol
        self.history = TimeSeries()
        self.update_event = Event()

    @property
    def price(self):
        """Returns the stocks most recent price.

        Returns:
            Most recent price.

        """
        try:
            return self.history[-1].value
        except IndexError:
            return None

    def update(self, timestamp, price):
        """Updates the stock's price history and fires an event.

        Args:
            timestamp (datetime.datetime): The timestamp of the update.
            price (optional[int, float]): The new price of the stock.

        Raises:
            ValueError: If price is less than zero.

        """
        if price < 0:
            raise ValueError("price should not be negative")
        self.history.update(timestamp, price)
        self.update_event.fire(self)

    @property
    def is_increasing_trend(self):
        """Determines if last three prices were ascending in value.

        Returns:
            True if there is an increasing trend, False if not.

        """
        return self.history[-3].value < self.history[-2].value < self.history[-1].value

    def _closing_price(self, on_date):
        """Returns a given dates closing price.

        This method was refactored to timeseries module. Remains for test maintenance.

        """
        return self.history.get_closing_price(on_date)

    @staticmethod
    def _is_crossover_below_to_above(on_date, ma, reference_ma):
        """Determines if the moving average given is crossing over its reference moving average on a given date.

        Args:
            on_date (datetime.datetime): The date on which the cross over signal is to be checked.
            ma (MovingAverage): The moving average.
            reference_ma (MovingAverage): The reference moving average.

        Returns:
            True if there is a crossover, False if not.

        """
        prev_date = on_date - timedelta(days=1)
        return (ma.value_on(prev_date) < reference_ma.value_on(prev_date) and
                ma.value_on(on_date) > reference_ma.value_on(on_date))

    def get_crossover_signal(self, on_date):
        """ Determines the appropriate crossover signal for a stock at a given date.

        There are three types of signals:
            Buy Signal: indicates the 5-day crosses 10-day moving average from below to above on that date.
            Sell Signal: indicates the 5-day crosses 10-day moving average from above to below on that date.
            Neutral Signal: indicates that there is not any crossover or insufficient price history data.

        Args:
            on_date (datetime.datetime): The date on which the cross over signal is to be checked.

        Returns:
            StockSignal.buy     : If there is a buy signal.
            StockSignal.sell    : If there is a sell signal.
            StockSignal.neutral : If there is a neutral signal, or there is insufficient price history data.

        """
        if self.history.has_sufficient_update_history(on_date, self.LONG_TERM_TIME_SPAN):
            return StockSignal.neutral

        long_term_moving_average = MovingAverage(self.history, self.LONG_TERM_TIME_SPAN)
        short_term_moving_average = MovingAverage(self.history, self.SHORT_TERM_TIME_SPAN)

        if self._is_crossover_below_to_above(on_date, short_term_moving_average, long_term_moving_average):
            return StockSignal.buy

        if self._is_crossover_below_to_above(on_date, long_term_moving_average, short_term_moving_average):
            return StockSignal.sell

        return StockSignal.neutral
