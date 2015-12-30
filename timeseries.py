import bisect
import collections

from datetime import timedelta

Update = collections.namedtuple("Update", ["timestamp", "value"])


class TimeSeries:
    def __init__(self):
        """An object that manages TimeSeries that include a timestamp and value.

        Attributes:
            series (Update): The chronological record of updates to the instance.

        """
        self.series = []

    def __getitem__(self, index):
        return self.series[index]

    def update(self, timestamp, value):
        """Updates the TimeSeries instance's series with a new entry.

        Args:
            timestamp: The timestamp of the update.
            value: The value of the update.
        """
        bisect.insort_left(self.series, Update(timestamp, value))

    def get_closing_price(self, on_date):
        """Returns a given dates closing price.

        This is the stock's last price from an update on the date or the closing price for the previous day if an
        update has not occurred.

        Args:
            on_date: The on_date being checked for a closing price.

        Raises:
            ValueError: If stock has not had any updates.

        Returns:
            Closing price if it exists, executes self.closing_price(previous day) if not.

        """
        if self.series:
            date_history = [update for update in self.series if update.timestamp.date() == on_date.date()]
            return date_history[-1].value if date_history else self.get_closing_price(on_date - timedelta(days=1))
        else:
            raise ValueError("stock has not had any updates")

    def has_sufficient_update_history(self, on_date, num_of_days):
        """Checks for sufficient update history data from a given date backwards with a given number of days.

        Args:
            on_date: The date on which the cross over signal is to be checked.
            num_of_days: The number of days of history.

        Returns:
            True if there is sufficient data, False if not.

        """
        earliest_date = on_date.date() - timedelta(days=num_of_days)
        return earliest_date < self.series[0].timestamp.date()
