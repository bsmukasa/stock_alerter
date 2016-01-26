class Event:
    def __init__(self):
        """A generic class that provides signal/slot functionality.

        Attributes:
            listeners: A list of functions registered for the event.

        """
        self.listeners = []

    def connect(self, listener):
        """Registers a listener function.

        Listener functions are registered for classes that want to get notified of the event when it is fired.

        Args:
            listener: The function of the class being registered.

        """
        self.listeners.append(listener)

    def fire(self, *args, **kwargs):
        """Fire the event notifying all registered functions.

        Each listener function is executed with arguments provided as parameters.

        Args:
            *args: Arguments to be used as parameters in the listener functions.
            **kwargs: Keyword arguments to be used as parameters in the listener functions.

        """
        for listener in self.listeners:
            listener(*args, **kwargs)
