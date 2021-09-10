class InvalidDateError(Exception):
    """Exception raised when an invalid date is entered."""

    def __init__(self, date: str, message: str):
        self.date = date
        self.message = message

    def __str__(self) -> str:
        return self.message + self.date