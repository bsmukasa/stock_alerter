class Processor:
    def __init__(self, reader, exchange):
        """Applies updates from a reader to an exchange of stocks.

        Args:
            reader: The source of stock updates.
            exchange: The list of stocks.

        """
        self.reader = reader
        self.exchange = exchange

    def process(self):
        """Executes all the updates in self.reader.

        """
        for symbol, timestamp, price in self.reader.get_updates():
            stock = self.exchange[symbol]
            stock.update(timestamp, price)
