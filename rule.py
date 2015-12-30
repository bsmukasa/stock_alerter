# -*- coding: utf-8 -*-
"""PriceRule class and associated features.

This module compares rules concerning a stock and its price history against a stock exchange record.

"""


class PriceRule:
    def __init__(self, symbol, condition):
        """PriceRule is a rule that triggers when a stock price satisfies a condition.

        The condition is usually greater, equal or lesser than a given value.

        Args:
            symbol (str): The stock's symbol.
            condition: The condition being checked.

        Attributes:
            symbol (str): The stock's symbol.
            condition: The condition being checked.

        """
        self.symbol = symbol
        self.condition = condition

    def matches(self, exchange):
        """Checks if there is a match in the stock exchange for the Rule instance.

        Args:
            exchange: The stock exchange being checked.

        Returns:
            True if there is a match in the exchange, False if not.

        Raises:
            KeyError: If self.symbol is not in the exchange.

        """
        try:
            stock = exchange[self.symbol]
        except KeyError:
            return False
        return self.condition(stock) if stock.price else False

    def depends_on(self):
        """Verifies that the Rule instance depends on its stock.

        Returns:
            True if the Rule instance depends on the stock, False if not.

        """
        return {self.symbol}


class AndRule:
    def __init__(self, *args):
        """A composite PriceRule class used for comparing multiple and/or composite PriceRules.

        Args:
            *args (Optional[PriceRule, AndRule]): The rules being checked.

        Attributes:
            *args (Optional[PriceRule, AndRule]): The rules being checked.

        """
        self.rules = args

    def matches(self, exchange):
        """Determines if there is a match between two rules.

        The two rules may be made of PriceRule instances or AndRule instances.

        Args:
            exchange: The stock exchange being checked.

        Returns:
            True if the AndRule finds matches in the exchange, False if not.

        """
        matches_bool = all([rule.matches(exchange) for rule in self.rules])
        return matches_bool

    def depends_on(self):
        depends = set()
        for rule in self.rules:
            depends = depends.union(rule.depends_on())
        return depends
