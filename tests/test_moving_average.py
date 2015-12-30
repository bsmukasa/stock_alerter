import unittest
from datetime import datetime

from moving_average import MovingAverage
from timeseries import TimeSeries


class StockCrossoverSignalTest(unittest.TestCase):
    def setUp(self):
        self.series = TimeSeries()
        self.series.update(datetime(2014, 4, 21), 42.63)
        self.series.update(datetime(2014, 4, 22), 78.39)
        self.series.update(datetime(2014, 4, 23), 71.54)
        self.current_ma = MovingAverage(self.series, 3)

    def test_calculation_of_three_day_moving_average(self):
        expected_moving_average = (42.63 + 78.39 + 71.54) / 3
        self.assertAlmostEquals(expected_moving_average, self.current_ma.value_on_date(datetime(2014, 4, 23)), places=4)
