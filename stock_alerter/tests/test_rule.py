from datetime import datetime
from unittest import TestCase

from stock import Stock

from stock_alerter.rule import PriceRule, AndRule


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
        redhat = Stock("RHT")
        redhat.update(datetime(2014, 2, 12), 7)
        apple = Stock("AAPL")
        apple.update(datetime(2014, 2, 13), 20)
        yahoo = Stock("YHOO")
        yahoo.update(datetime(2014, 2, 14), 9)
        cls.exchange = {"GOOG": goog, "MSFT": msft, "RHT": redhat, "AAPL": apple, "YHOO": yahoo}

    def test_an_AndRule_matches_if_all_component_rules_are_true(self):
        """Tests if True is returned if all component rules of a AndRule are true.

        """
        rule = AndRule(PriceRule("GOOG", lambda stock: stock.price > 8),
                       PriceRule("MSFT", lambda stock: stock.price > 10))
        self.assertTrue(rule.matches(self.exchange))

    def test_an_AndRule_matches_if_all_component_rules_are_not_true(self):
        """Tests if False is returned if all component rules of a AndRule are not true.

        """
        rule = AndRule(PriceRule("GOOG", lambda stock: stock.price < 8),
                       PriceRule("MSFT", lambda stock: stock.price > 10))
        self.assertFalse(rule.matches(self.exchange))

    def test_an_AndRule_true_matches_if_one_component_is_an_AndRule(self):
        """Tests if True is returned if all component rules of a AndRule are true and one component is an AndRule.

        """
        and_rule = AndRule(PriceRule("GOOG", lambda stock: stock.price > 8),
                           PriceRule("MSFT", lambda stock: stock.price > 10))
        rule = AndRule(and_rule, PriceRule("RHT", lambda stock: stock.price > 5))
        self.assertTrue(rule.matches(self.exchange))

    def test_an_AndRule_false_matches_if_one_component_is_an_AndRule(self):
        """Tests if False is returned if all component rules of a AndRule are false and one component is an AndRule.

        """
        and_rule = AndRule(PriceRule("GOOG", lambda stock: stock.price > 8),
                           PriceRule("MSFT", lambda stock: stock.price > 10))
        rule = AndRule(and_rule, PriceRule("RHT", lambda stock: stock.price < 5))
        self.assertFalse(rule.matches(self.exchange))

    def test_an_AndRule_true_matches_if_components_made_of_several_AndRules(self):
        """Tests if True is returned if all component rules of a AndRule are compound AndRules.

        """
        and_rule1 = AndRule(PriceRule("GOOG", lambda stock: stock.price > 8),
                            PriceRule("MSFT", lambda stock: stock.price > 10))
        and_rule2 = AndRule(and_rule1, PriceRule("RHT", lambda stock: stock.price > 5))
        and_rule3 = AndRule(PriceRule("AAPL", lambda stock: stock.price > 19),
                            PriceRule("YHOO", lambda stock: stock.price < 10))
        rule = AndRule(and_rule2, and_rule3)
        self.assertTrue(rule.matches(self.exchange))
