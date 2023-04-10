import locale
import textwrap
from datetime import datetime
from typing import Any, Dict, ItemsView, List

import ConfigurationProcessor as Conf

conf = Conf.ConfigurationProcessor()

locale.setlocale(conf.get_property("LOCALE"), '')  # set the locale for printing the amount

# the Keys used for the Transaction and printing the transaction
KEYS = ["Date", "Trans", "Category", "Desc", "Amount", "Num"]

def _build_template():
    template = ""
    template += conf.get_property("VLINE_CHAR")
    for i in range(len(KEYS)):
        header_length = conf.get_property("SIZE_LIST")[i]
        format_string = '{' + KEYS[i] + ':^' + str(header_length) + '}'
        template += format_string + conf.get_property("VLINE_CHAR")


    return template

TRANSACTION_ROW_PRINT_TEMPLATE = _build_template()

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
            insert_val = datetime.strptime(value, conf.get_property("DATE_FORMAT")).date()
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

    @classmethod
    def set_uid(cls, value: int) -> None:
        cls._uid = value    

    def _wrap_text(self, text: str, length: int) -> List[str]:
        wrapped_text = textwrap.wrap(text, width=length)

        if(len(text) > length):
            pass

        return wrapped_text
    
    def _create_default_row(self) -> Dict[str, str]:
        default_row :Dict[str, str] = {}
        for key in KEYS:
            default_row[key] = ""

        return default_row

    def _get_row_for_index(self, rows_to_create :List[Dict[str, str]], index :int) -> Dict[str, str]:
        row :Dict[str, str] = {}

        if(len(rows_to_create) == index):
            rows_to_create.append(self._create_default_row())

        row = rows_to_create[index]

        return row

    def _fill_in_rows(self, rows_to_create :List[Dict[str, str]], key: str, text_to_wrap: List[str]) -> None:
        for i in range(len(text_to_wrap)):
            current_row = self._get_row_for_index(rows_to_create, i)
            current_row[key] = text_to_wrap[i]

    def _wrap_transaction_text(self, transaction_vals :Dict[str, str]) -> str:
        wrapped_text = ""
        rows_to_create :List[Dict[str, str]] = []

        for i in range(len(KEYS)):
            text_after_wrap = textwrap.fill(transaction_vals[KEYS[i]], width=conf.get_property("SIZE_LIST")[i]).split("\n")
            self._fill_in_rows(rows_to_create, KEYS[i], text_after_wrap)

        for row in rows_to_create:
            wrapped_text += TRANSACTION_ROW_PRINT_TEMPLATE.format(**row) + "\n"


        return wrapped_text.strip()

    def __str__(self):
        """A string representation of a Checkbook Transaction"""
        string = conf.get_property("VLINE_CHAR")
        transaction_vals = {}
        for i in range(len(KEYS)):
            header_length = conf.get_property("SIZE_LIST")[i]
            format_string = '{:^' + str(header_length) + '}'
            val = self.data.get(KEYS[i])
            if type(val) is datetime:
                val = datetime.strftime(self.get_value(KEYS[i]), conf.get_property("DATE_FORMAT")) #self.data.get(KEYS[i])
            elif type(val) is float:
                val = locale.currency(val, grouping=conf.get_property("THOUSAND_SEP"))
    
            string += format_string.format(str(val)) + conf.get_property("VLINE_CHAR")
            transaction_vals[KEYS[i]] = str(val)


        string = self._wrap_transaction_text(transaction_vals)
        return string

    def __eq__(self, __o: object) -> bool:
        areEqual = True
        if isinstance(__o, CheckbookTransaction):
            for val in KEYS:
                if val != "Num":
                    thisVal = self.get_value(val)
                    otherVal = __o.get_value(val)
                    if thisVal != otherVal:
                        areEqual = False
                        break
        else:
            areEqual = False

        return areEqual
