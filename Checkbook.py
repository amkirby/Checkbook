import locale
from typing import Any, Callable, List, Optional

import CheckbookTransaction as CBT
import ConfigurationProcessor as Conf
from DateProcessor import DateProcessor

conf = Conf.ConfigurationProcessor()

ROW_SEP = '\n' + (conf.get_property("HLINE_CHAR") * (sum(conf.get_property("SIZE_LIST")) + len(conf.get_property("SIZE_LIST")))) + '\n'


class Checkbook:
    """A class that represents a checkbook

    Attributes:
        check_register (list) : contains instances of CheckbookTransaction
    """

    def __init__(self):
        """Initializes an empty check register"""
        self.check_register: List[CBT.CheckbookTransaction] = []
        self.file_name: str = conf.get_property("FILE_NAME")
        self.edited: bool = False

    def create_based_on_list(self, cbt_list: List[CBT.CheckbookTransaction]) -> None:
        self.check_register = cbt_list

    def add(self, cbt_list: List[CBT.CheckbookTransaction]) -> None:
        """Adds the specified list to the checkbook

        Args:
            cbt_list (list) : contains values in the order of the CBT.KEYS that
                             are used to create a transaction
        """
        cbt = CBT.CheckbookTransaction()
        for i in range(len(cbt_list)):
            cbt.set_value(CBT.KEYS[i], cbt_list[i])
        self.check_register.append(cbt)
        self.edited = True

    def add_single_trans(self, cbt: CBT.CheckbookTransaction) -> None:
        """Adds a CheckbookTransaction to the register

        Args:
             cbt (CheckbookTransaction) : the CBT to be added to the checkbook
        """
        self.check_register.append(cbt)
        self.edited = True

    def load(self, file_name: str, load_function: Callable[[str], List[CBT.CheckbookTransaction]]) -> None:
        """Tries to load the specified file name into the check register

        Args:
            file_name (string) : the file to load into the checkbook
            load_function (function): function used to save the checkbook
        """
        self.file_name = file_name
        self.check_register = load_function(self.file_name)

    def clear(self) -> None:
        """Clears the checkbook"""
        del self.check_register[:]
        CBT.CheckbookTransaction.reset_uid()

    def save(self, save_function: Callable[[str, List[CBT.CheckbookTransaction]], None]) -> None:
        """Saves the checkbook in XML format

        Args:
            save_function (function): function used to save the checkbook
        """
        save_function(self.file_name, self.check_register)
        self.edited = False

    def is_edited(self) -> bool:
        """Returns if the checkbook has been edited

        Returns:
            boolean: True if checkbook has been edited, False otherwise
        """
        return self.edited

    def set_edited(self, edit: bool) -> None:
        """Sets the edited status to the specified value

        Args:
            edit (boolean) : the state to set if the checkbook is edited
        """
        self.edited = edit

    def get_transaction_type(self, trans_type: str) -> List[CBT.CheckbookTransaction]:
        """Gets all transactions with the specified trans type

        Args:
            trans_type (string) : the transaction type to gather

        Returns:
            list: a list of transactions with the specified trans type
        """
        return_list: List[CBT.CheckbookTransaction] = []
        for elem in self.check_register:
            if elem.get_dictionary().get("Trans") == trans_type:
                return_list.append(elem)
        return return_list

    def get_category(self, cat: str) -> List[CBT.CheckbookTransaction]:
        """Gets all transactions with the specified category

        Args:
            cat (string) : the category to gather

        Returns:
            list: a list of transactions with the specified category
        """
        return_list: List[CBT.CheckbookTransaction] = []
        cat_list = [x.strip() for x in cat.split(",")]
        for category in cat_list:
            for elem in self.check_register:
                if str(elem.get_dictionary().get("Category")).lower() == category.lower():
                    return_list.append(elem)
        return return_list

    def get_month(self, date_processor: DateProcessor) -> List[CBT.CheckbookTransaction]:
        """Gets all transactions with the specified month

        Args:
            date_processor (DateProcessor): The date range
        Returns:
            list: a list of transactions with the specified month
        """

        return_list: List[CBT.CheckbookTransaction] = []
        for elem in self.check_register:
            date: Any = elem.get_dictionary().get("Date")
            if (date_processor.date_within_range(date)): 
                return_list.append(elem)
        return return_list

    def _process_date_range(self, month_str: str):
        month_start = 1
        month_end = 12
        year_start = 1998
        year_end = 9999

        vals = month_str.split() # separate month and year by spaces
        if(len(vals) == 1):
            # could be month (range) or year (range)
            ranges = vals[0].split("-")
            ranges = [int(i) for i in ranges]
            if(ranges[0] >= 1 and ranges[0] <= 12):
                #month value
                month_start, month_end = self._get_start_end_values(ranges)
            else:
                # assumed year value
                year_start, year_end = self._get_start_end_values(ranges)
        elif(len(vals) == 2):
            # both month (range) and year (range)
            month_ranges = vals[0].split("-")
            month_ranges = [int(i) for i in month_ranges]
            year_ranges = vals[1].split("-")
            year_ranges = [int(i) for i in year_ranges]

            month_start, month_end = self._get_start_end_values(month_ranges)
            year_start, year_end = self._get_start_end_values(year_ranges)


        return month_start, month_end, year_start, year_end

    def _get_start_end_values(self, ranges : List[int]):
        start = -1
        end = -1

        if(len(ranges) == 1):
            start = end = ranges[0]
        else:
            start = ranges[0]
            end = ranges[1]


        return start, end

    def _validate_date_ranges(self, month_start: int, month_end: int, year_start: int, year_end: int) -> bool:
        is_valid = True
        month_valid = False
        year_valid = False
        if(month_start <= month_end and 1 <= month_start <= 12 and 1 <= month_end <= 12):
            month_valid = True
        if(year_start <= year_end and 1998 <= year_start <= 9999 and 1998 <= year_end <= 9999):
            year_valid = True
        
        is_valid = month_valid and year_valid

        return is_valid

    def get_description(self, search_term: str) -> List[CBT.CheckbookTransaction]:
        return_list: List[CBT.CheckbookTransaction] = []
        if(type(search_term) is not str):
            search_term = str(search_term)
        for cbt in self.check_register:
            transaction_desc = str(cbt.get_value("Desc"))
            if(search_term.lower() in transaction_desc.lower()):
                return_list.append(cbt)

        return return_list

    def get_total_for_trans(self, trans: str) -> float:
        """Get the total amount for the specified trans type

        Args:
            trans (string) : the transaction type that is totaled

        Returns:
            float: Total amount for the specified trans type
        """
        trans_list = self.get_transaction_type(trans)
        total = 0.0
        for elem in trans_list:
            total += elem.get_amount()
        return total

    def get_total_for_trans_month(self, trans: str, date_processor: DateProcessor) -> float:
        """Get the total for the specified transaction in the specified month

        Args:
            trans (string) : the transaction type to total
            date_processor (DateProcessor): The date range

        Returns:
            float: Total amount for the specified trans type for the specified month
        """
        month_list = self.get_month(date_processor)
        total = 0.0
        for elem in month_list:
            if elem.get_value("Trans") == trans:
                total += elem.get_amount()
        return total

    def get_total_for_cat(self, category: str) -> float:
        """Get the total for the specified category

        Args:
            category (string) : The category to total

        Returns:
            float: Total amount for the specified category
        """
        cat_list = self.get_category(category)
        total = 0.0
        for elem in cat_list:
            total += elem.get_amount()
        return total

    def get_total(self) -> float:
        """Gets the total for the register

        Returns:
            float: Total amount for the checkbook
        """
        total = 0.0
        for elem in self.check_register:
            total += elem.get_amount()
        return total

    def find_transaction(self, in_trans: int) -> CBT.CheckbookTransaction:
        """Gets the specified transaction number from the register

        Args:
            in_trans (int) : the transaction to gather

        Returns:
            CheckbookTransaction: The specified transaction
        """
        transaction: Any = None #CBT.CheckbookTransaction()
        for currentTrans in self.check_register:
            if int(currentTrans.get_value("Num")) == in_trans:
                transaction = currentTrans
        return transaction

    def get_file_name(self) -> str:
        return self.file_name

    def _gen_total_line_print(self) -> str:
        """creates the total line at the bottom of the register

        Returns:
            str: The total line for the checkbook
        """
        string = conf.get_property("VLINE_CHAR")
        # format total: text
        format_string = '{:>' + str(sum(conf.get_property("SIZE_LIST")[:-2]) + 4) + '}'
        string += format_string.format("Total : ")
        # format amount
        format_string = '{:^' + str((conf.get_property("SIZE_LIST")[-2])) + '}'
        string += format_string.format(locale.currency(self.get_total(), grouping=conf.get_property("THOUSAND_SEP")))
        # format final bar
        format_string = '{:>' + str((conf.get_property("SIZE_LIST")[-1]) + 2) + '}'
        string += format_string.format(conf.get_property("VLINE_CHAR"))
        return string

    def _gen_header_print(self) -> str:
        """Creates the header line at the top of the register

        Returns:
            str: The header line for the checkbook
        """
        header = ROW_SEP
        header += conf.get_property("VLINE_CHAR")
        for i in range(len(CBT.KEYS)):
            header_length = conf.get_property("SIZE_LIST")[i]
            format_string = '{:^' + str(header_length) + '}'
            header += format_string.format(CBT.KEYS[i]) + conf.get_property("VLINE_CHAR")
        return header

    def _gen_trans_print(self, print_list: Optional[List[CBT.CheckbookTransaction]]=None) -> str:
        """Creates the print for each transaction in the register

        Args:
            print_list (list) : the list of CBTs to loop through to generate
                               the transaction print. If None, loop through 
                               the whole checkbook

        Returns:
            str: The print for the transactions in the checkbook
        """
        iter_list: List[CBT.CheckbookTransaction] = []
        if print_list is None:
            iter_list = self.check_register
        else:
            iter_list = print_list

        string = ''
        for elem in iter_list:
            string += str(elem)
            string += ROW_SEP
        return string

    def get_specific_print(self, key: str, value: Any) -> str:
        """Print a subset of the checkbook

        Args:
            key (string) : the key to to get the subset from
            value (int | string) : the value from key to get

        Returns:
            str: The print for a subset of transactions based on the specified input
        """
        string = self._gen_header_print()
        string += ROW_SEP
        string += self._gen_trans_print(self.get_specific_list(key, value))
        return string

    def get_specific_list(self, key: str, value: Any) -> List[CBT.CheckbookTransaction]:
        """Gets the subset list based on the given input

        Args:
            key (string) : the key to to get the subset from
            value (int | string) : the value from key to get

        Returns:
            list: A list of a subset of transactions based on the specified input
        """
        func = self.specific_print_functions[key.capitalize()]
        func_param: Any = None
        if "Date" == key.capitalize():
            func_param = DateProcessor(value)
        elif value.isdigit():
            func_param = int(value)
        else:
            func_param = value.capitalize()

        return_list = func(self, func_param)

        return return_list

    def get_register(self):
        return self.check_register

    def order_by(self, key: str):
        self.check_register.sort(key=lambda cbt: cbt.get_value(key))

    def __str__(self):
        """A string representation of a checkbook

        Returns:
            str: The print for the checkbook
        """
        string = self._gen_header_print()
        string += ROW_SEP
        string += self._gen_trans_print()
        string += self._gen_total_line_print()
        string += ROW_SEP
        return string

    specific_print_functions = {
        "Date": get_month,
        "Trans": get_transaction_type,
        "Category": get_category,
        "Desc": get_description
    }
