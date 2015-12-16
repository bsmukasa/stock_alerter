class PriceRule:
    """PriceRule is a rule that triggers when a stock price satisfies a condition.

    The condition is usually greater, equal or lesser than a given value.
    """

    def __init__(self, symbol, condition):
        self.symbol = symbol
        self.condition = condition

    def matches(self, exchange):
        try:
            stock = exchange[self.symbol]
        except KeyError:
            return False
        return self.condition(stock) if stock.price else False

    def depends_on(self):
        return {self.symbol}


class AndRule:
    def __init__(self, rule1, rule2):
        self.rule1 = rule1
        self.rule2 = rule2
