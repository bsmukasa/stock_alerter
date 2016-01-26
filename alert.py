class Alert:
    def __init__(self, description, rule, action):
        """Maps a Rule object to an Action, and triggers it when appropriate.

        Triggers the action if the rule matches on any stock update.

        Args:
            description (str): Brief description of the alert.
            rule (Rule): The rule the alert is checking.
            action (Action): The action taken if the rule is matched.

        Attributes:
            description (str): Brief description of the alert.
            rule (Rule): The rule the alert is checking.
            action (Action): The action taken if the rule is matched.
            exchange: The list of dependent stocks added when connect is executed.
        """
        self.description = description
        self.rule = rule
        self.action = action
        self.exchange = None

    def connect(self, exchange):
        """ Connects all dependent stocks to their updated event.

        The updated Event instance is fired whenever a new update is made to a stock. The listener for this event
        is the self.check_rule method of the Alert class.

        Args:
            exchange: The list of dependent stocks.
        """
        self.exchange = exchange
        dependent_stocks = self.rule.depends_on()
        for stock in dependent_stocks:
            exchange[stock].updated.connect(self.check_rule)

    def check_rule(self):
        """ Checks if a stock's update causes a rule to be matched.

        If the rule is matched, it calls the execute method on the Action
        instance. If the rule doesn't match, then nothing happens.
        """
        if self.rule.matches(self.exchange):
            self.action.execute(self.description)
