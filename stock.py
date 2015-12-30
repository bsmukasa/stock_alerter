from datetime import timedelta
from enum import Enum
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

        """
        self.symbol = symbol
        self.price_history = []
        self.history = TimeSeries()

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
        """Updates the stock's price history.

        Args:
            timestamp: The timestamp of the update.
            price: The new price of the stock.

        Raises:
            ValueError: If price is less than zero.

        """
        if price < 0:
            raise ValueError("price should not be negative")
        self.history.update(timestamp, price)

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

    def _moving_average(self, on_date, num_of_days):
        """Calculates the moving average of a stock's closing prices from a given on_date.

        Args:
            on_date: The on_date from which the moving average is being calculated.
            num_of_days: The number of days to be averaged.

        Returns:
            The average closing price for the given range if there are sufficient days in price history, 0 if not.

        """
        dates = [on_date - timedelta(days=i) for i in range(num_of_days)]
        closing_prices = [self.history.get_closing_price(date) for date in dates]
        average_closing_price = sum(closing_prices) / num_of_days
        return average_closing_price

    def _date_in_price_history(self, on_date, num_of_days):
        """Checks it a provided date range exists in a stock's price history.

        Args:
            on_date: The end date of the date range.
            num_of_days: The number of days in the date range.

        Returns:
            True if the date exists, False if not.

        """
        earliest_date = on_date.date() - timedelta(days=num_of_days)
        return earliest_date > self.history[0].timestamp.date()

    def _is_insufficient_price_history_data(self, on_date):
        """Checks for sufficient previous price history data from a given date to execute self.get_crossover_signal.

        Args:
            on_date: The date on which the cross over signal is to be checked.

        Returns:
            True if there is sufficient data, False if not.

        """
        earliest_date = on_date.date() - timedelta(days=self.LONG_TERM_TIME_SPAN)
        return earliest_date < self.history[0].timestamp.date()

    @staticmethod
    def _is_short_term_crossover_below_to_above(prev_ma, prev_reference_ma, current_ma, current_reference_ma):
        return prev_ma < prev_reference_ma and current_ma > current_reference_ma

    def get_crossover_signal(self, on_date):
        """ Determines the appropriate crossover signal for a stock at a given date.

        There are three types of signals:
            Buy Signal: indicates the 5-day crosses 10-day moving average from below to above on that date.
            Sell Signal: indicates the 5-day crosses 10-day moving average from above to below on that date.
            Neutral Signal: indicates that there is not any crossover or insufficient price history data.

        Args:
            on_date: The date on which the cross over signal is to be checked.

        Returns:
            1 : If there is a buy signal.
            -1: If there is a sell signal.
            0 : If there is a neutral signal, or there is insufficient price history data.

        """
        if self._is_insufficient_price_history_data(on_date):
            return StockSignal.neutral

        long_term_moving_average = self._moving_average(on_date, self.LONG_TERM_TIME_SPAN)
        short_term_moving_average = self._moving_average(on_date, self.SHORT_TERM_TIME_SPAN)
        prev_long_term_moving_average = self._moving_average(on_date - timedelta(days=1), self.LONG_TERM_TIME_SPAN)
        prev_short_term_moving_average = self._moving_average(on_date - timedelta(days=1), self.SHORT_TERM_TIME_SPAN)

        if self._is_short_term_crossover_below_to_above(
                prev_short_term_moving_average, prev_long_term_moving_average,
                short_term_moving_average, long_term_moving_average
        ):
            return StockSignal.buy

        if self._is_short_term_crossover_below_to_above(
                prev_long_term_moving_average, prev_short_term_moving_average,
                long_term_moving_average, short_term_moving_average
        ):
            return StockSignal.sell

        return StockSignal.neutral
