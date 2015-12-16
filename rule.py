class PriceRule:
    """PriceRule is a rule that triggers when a stock price satisfies a condition.

    The condition is usually greater, equal or lesser than a given value.
    """

    def __init__(self, symbol, condition):
        self.symbol = symbol
        self.condition = condition
