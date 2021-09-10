import locale
from datetime import datetime
from typing import Any, Dict, ItemsView

from Constants import config
from Constants import printConstants as PC

locale.setlocale(config.LOCALE, '')  # set the locale for printing the amount

# the Keys used for the Transaction and printing the transaction
KEYS = ["Date", "Trans", "Category", "Desc", "Amount", "Num"]


class CheckbookTransaction:
    """This class represents a Checkbook Transaction

    Class Variables:
        UID : an identifier for the transaction

    Attributes:
        data : a dictionary to contain the transaction
    """
    _uid = 1  # The current transaction number

    def __init__(self):
        """Creates an empty transaction with the next available UID"""
        self.data: Dict[str, Any] = dict()
        for elem in KEYS:
            self.data[elem] = None
        self.data[KEYS[-1]] = CheckbookTransaction._uid
        CheckbookTransaction._uid += 1

    def get_items(self) -> ItemsView[str, Any]:
        """Gets the key, value of the transaction

        Returns:
            iterable tuple: key, value pairs of the transaction
        """
        return self.data.items()

    def get_dictionary(self) -> Dict[str, Any]:
        """Gets the data as a dictionary

        Returns:
            dict: the dictionary of the transaction
        """
        return self.data

    def get_amount(self) -> Any:
        """Gets the amount of the transaction

        Returns:
            float: the amount value of the transaction
        """
        return self.data.get("Amount")

    def get_value(self, key: str) -> Any:
        """Gets the value of the specified key

        Args:
            key (string) : the key to gather

        Returns:
            object: the value associated with the specified key
        """
        return self.data.get(key)

    def get_date(self) -> datetime:
        """Get the value of the Date key

        Returns:
            datetime: The date value of the transaction
        """
        return self.get_value("Date")

    def set_value(self, key: str, value: Any) -> None:
        """Sets the specified key with the specified value

        Args:
            key (string)   : the key to set
            value (string) : the value to set with key
        """
        insert_val = value
        if key == "Date":
            insert_val = datetime.strptime(value, config.DATE_FORMAT).date()
        elif key == "Amount":
            insert_val = float(value)
        self.data[key] = insert_val

    def is_debit(self) -> bool:
        return self.data.get("Trans") == "Debit"

    @classmethod
    def reset_uid(cls) -> None:
        """A class method that resets the _UID"""
        cls._uid = 1

    @classmethod
    def decrement_uid(cls) -> None:
        cls._uid = cls._uid - 1    

    def __str__(self):
        """A string representation of a Checkbook Transaction"""
        string = PC.VLINE_CHAR
        for i in range(len(KEYS)):
            header_length = PC.SIZE_LIST[i]
            format_string = '{:^' + str(header_length) + '}'
            val = self.data.get(KEYS[i])
            if type(val) is datetime:
                val = datetime.strftime(self.get_value(KEYS[i]), config.DATE_FORMAT) #self.data.get(KEYS[i])
            elif type(val) is float:
                val = locale.currency(val, grouping=config.THOUSAND_SEP)
            string += format_string.format(str(val)) + PC.VLINE_CHAR
        return string
