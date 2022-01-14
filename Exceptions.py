from Constants import commands, config

class InvalidDateError(Exception):
    """Exception raised when an invalid date is entered."""

    def __init__(self, date: str, message: str):
        self.date = date
        self.message = message

    def __str__(self) -> str:
        return self.message + self.date + " -> (expected " + config.DATE_FORMAT + ")"

class InvalidMonthError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.month = args[0]
        self.message = args[1]
    
    def __str__(self) -> str:
        return str(self.message) + str(self.month) + " -> (expected month : 1-12 year : 1998-9999)"

class InvalidCommandError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.command = args[0]
        self.message = args[1]

    def __str__(self) -> str:
        return str(self.message) + str(self.command) + commands.COMMAND_HELP
    
class InvalidAmountError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.amount = args[0]
        self.message = args[1]

    def __str__(self) -> str:
        return str(self.message) + str(self.amount) + " -> (expected XXXX.XX)"