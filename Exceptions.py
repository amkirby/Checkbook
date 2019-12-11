class InvalidDateError(Exception):
    """Exception raised when an invalid date is entered."""

    def __init__(self, date, message):
        self.date = date
        self.message = message

    def __str__(self):
        return self.message + self.date