from datetime import datetime


class ListReader:
    def __init__(self, updates):
        """A reader using a list source from where stock updates are coming.

        Args:
            updates: List of stock updates.

        """
        self.updates = updates

    def get_updates(self):
        """A generator returning each stock update from the list reader.

        """
        for update in self.updates:
            yield update


class FileReader:
    def __init__(self, filename):
        """A reader using a file source from where stock updates are coming.

        Args:
            filename (str): The name of the file containing the stock updates.

        """
        self.filename = filename

    def get_updates(self):
        """A generator returning each stock update from the file reader.

        """
        with open(self.filename, "r") as fp:
            data = fp.read()
            lines = data.split()
            for line in lines:
                symbol, timestamp, price = line.split(",")
                yield (
                    symbol,
                    datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f"),
                    int(price)
                )
