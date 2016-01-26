from datetime import timedelta


class MovingAverage:
    def __init__(self, series, time_span):
        """Constructor for the MovingAverage object.

        Args:
            series: The series of numbers used to calculate moving averages including timestamps and values.
            time_span (int): The length number of items from the series used in calculating a moving average.

        Attributes:
            series: The series of numbers used to calculate moving averages including timestamps and values.
            time_span (int): The length number of items from the series used in calculating a moving average.

        """
        self.series = series
        self.time_span = time_span

    def value_on(self, on_date):
        """Calculates the moving average of a stock's closing prices from a given on_date.

        Args:
            on_date (datetime.datetime): The on_date from which the moving average is being calculated.

        Returns:
            The average closing price for the given range if there are sufficient days in price history, 0 if not.

        """
        dates = [on_date - timedelta(days=i) for i in range(self.time_span)]
        closing_prices = [self.series.get_closing_price(date) for date in dates]
        average_closing_price = sum(closing_prices) / self.time_span
        return average_closing_price
