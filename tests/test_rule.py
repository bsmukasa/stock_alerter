from datetime import datetime
from unittest import TestCase

from rule import PriceRule, AndRule
from stock import Stock


class TestPriceRule(TestCase):
    @classmethod
    def setUpClass(cls):
        goog = Stock("GOOG")
        goog.update(datetime(2014, 2, 10), 11)
        cls.exchange = {"GOOG": goog}

    def test_a_PriceRule_matches_when_it_meets_the_condition(self):
        """Tests if true is returned when an exchange matches a rule.

        """
        rule = PriceRule("GOOG", lambda stock: stock.price > 10)
        self.assertTrue(rule.matches(self.exchange))

    def test_a_PriceRule_is_False_if_the_condition_is_not_met(self):
        """Tests if false is returned when an exchange does not match a rule.

        """
        rule = PriceRule("GOOG", lambda stock: stock.price < 10)
        self.assertFalse(rule.matches(self.exchange))

    def test_a_PriceRule_is_False_if_the_stock_is_not_in_the_exchange(self):
        """Tests if false is returned if a match is attempted when the stock is not in the exchange.

        """
        rule = PriceRule("MSFT", lambda stock: stock.price > 10)
        self.assertFalse(rule.matches(self.exchange))

    def test_a_PriceRule_is_False_if_the_stock_hasnt_got_an_update_yet(self):
        """Tests if false is returned if matched stock has not had an update.

        """
        self.exchange["AAPL"] = Stock("AAPL")
        rule = PriceRule("AAPL", lambda stock: stock.price > 10)
        self.assertFalse(rule.matches(self.exchange))

    def test_a_PriceRule_only_depends_on_its_stock(self):
        """Test if a rule only depends on its stock.

        """
        rule = PriceRule("MSFT", lambda stock: stock.price > 10)
        self.assertEqual({"MSFT"}, rule.depends_on())


class TestAndRule(TestCase):
    @classmethod
    def setUpClass(cls):
        goog = Stock("GOOG")
        goog.update(datetime(2014, 2, 10), 11)
        msft = Stock("MSFT")
        msft.update(datetime(2014, 2, 11), 12)
        cls.exchange = {"GOOG": goog, "MSFT": msft}

    def test_an_AndRule_matches_if_all_component_rules_are_true(self):
        """Tests True is returned if all component rules of a AndRule are true.

        """
        rule = AndRule(PriceRule("GOOG", lambda stock: stock.price > 8),
                       PriceRule("MSFT", lambda stock: stock.price > 10))
        self.assertTrue(rule.matches(self.exchange))
