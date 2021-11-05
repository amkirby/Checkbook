import string
from typing import Any, Callable, List, Optional
import CheckbookTransaction as CBT
import Checkbook as CB
import checkbookReport as CR
from Exceptions import *
from Constants import commands
from Constants import config


def _apply_debit_multiplier(debit_transaction: CBT.CheckbookTransaction) -> None:
    if((debit_transaction.is_debit() and int(debit_transaction.get_amount()) > 0)
        or (not debit_transaction.is_debit() and int(debit_transaction.get_amount()) < 0)):
        debit_transaction.set_value("Amount", debit_transaction.get_amount() * config.DEBIT_MULTIPLIER)

class CommandProcessor:
    """A class to process commands entered by the user. A function should be
    passed to each method to do the actual processing.
    ****NOTE: Each passed function is expected to take a Checkbook object as a parameter.
    ****NOTE: The separate methods remain to facilitate inheritance if desired.

    Attributes:
        checkbook (Checkbook) : the current checkbook the user is using
    """

    def __init__(self, checkbook: CB.Checkbook):
        """Initializes the checkbook that will be used for the operations

        Args:
            checkbook (Checkbook) : the checkbook to operate on
        """
        self.checkbook = checkbook
        self._trans_selection = ""

    def _do_save(self, save_function: Callable[[str, List[CBT.CheckbookTransaction]], None]) -> None:
        """Saves the checkbook

        Args:
            save_function (function): function used to save the checkbook
        """
        save = input("Would you like to save? (y or n) ")
        if save.lower() == "y":
            self.checkbook.save(save_function)
            print("save successful!")

    def _select_with_number(self, text_list: List[str], key: str, def_text: Optional[Any]=None) -> str:
        """Select a value from the given list by using it's index

        Args:
            text_list (list) : a list of strings to Select
            key (str)        : a prompt for input
            def_text (str)   : default text to display

        Returns:
            (str) : the chosen value from the given list
        """
        max_len = len(max(text_list, key=len))
        format_string = "{:<" + str(max_len) + "}"
        prev_text = ""
        if def_text is not None:
            prev_text = "(" + str(def_text) + ")"

        for i in range(len(text_list)):
            print("  " + format_string.format(text_list[i]), i)
        val = input(key + prev_text + " : ")
        if val.strip() != "" and val.isdigit() and (0 <= int(val) < len(text_list)):
            val = text_list[int(val)]
        return val

    def process_add_command(self) -> None:
        """Adds a transaction to the checkbook"""
        print("Enter your transaction")
        cbt = CBT.CheckbookTransaction()
        val = ""
        try:
            for key in CBT.KEYS:
                if key != "Num":
                    if key == "Category":
                        val = self._select_with_number(config.CATEGORIES_FOR_ADD[self._trans_selection], key)
                    elif key == "Trans":
                        val = self._select_with_number(commands.TRANS_TYPES, key)
                        self._trans_selection = val
                    else:
                        val = input(key + " : ")

                    cbt.set_value(key, string.capwords(val))
        except ValueError as e:
            CBT.CheckbookTransaction.decrement_uid()
            if "time data" in repr(e):
                error = InvalidDateError(val, "Invalid date entered of: ")
                raise error
            elif "convert string to float" in repr(e):
                error = InvalidAmountError(val, "Invalid amount entered : ")
                raise error
            else:
                raise e

        _apply_debit_multiplier(cbt)
        self.checkbook.add_single_trans(cbt)

    def process_edit_command(self, *args: str) -> None:
        """Edit a transaction

        Args:
            *args (variable args): Can pass an int which specifies the transaction to edit
        """
        if not args:
            edit_trans = int(input("Which transaction do you want to edit? : "))
        else:
            edit_trans = int(args[0])

        trans = self.checkbook.find_transaction(edit_trans)
        for key in CBT.KEYS:
            if key != "Num":
                if key == "Category":
                    val = self._select_with_number(config.CATEGORIES_FOR_ADD[self._trans_selection], key, trans.get_value(key))
                elif key == "Trans":
                    val = self._select_with_number(commands.TRANS_TYPES, key, trans.get_value(key))
                    self._trans_selection = val
                else:
                    val = input(key + " (" + str(trans.get_value(key)) + ")" + " : ")
                if val.strip() != "":
                    trans.set_value(key, string.capwords(val))
                    self.checkbook.set_edited(True)

        _apply_debit_multiplier(trans)

    def process_report_command(self):
        """Generate a report"""
        format_string = "{:<8}"
        month = None
        print("Report Types:")
        for i in range(len(CR.REPORT_TYPES)):
            print(format_string.format(CR.REPORT_TYPES[i]), ":", i)
        rep_type = int(input("Enter desired report number : "))
        cr = CR.CheckbookReport(self.checkbook)
        rep_method = CR.CheckbookReport.dispatcher[CR.REPORT_TYPES[rep_type]]
        if rep_type == 0:
            month = int(input("Enter desired month as a number : "))

        report_text = rep_method(cr, month)
        print(report_text)

    def process_load_command(self, load_function: Callable[[str], List[CBT.CheckbookTransaction]], *args: str) -> None:
        """Load another checkbook

        Args:
            load_function (function): function used to save the checkbook
            *args (variable args)   : Can specify the checkbook to load
        """
        file_name: str = ""
        if not args:
            file_name = input("Enter an XML file to load : ")
        else:
            file_name = args[0]

        self.checkbook.clear()
        self.checkbook.load(file_name, load_function)

    def process_save_command(self, save_function: Callable[[str, List[CBT.CheckbookTransaction]], None]) -> None:
        """Save the checkbook

        Args:
            save_function (function): function used to save the checkbook
        """
        if self.checkbook.is_edited():
            self._do_save(save_function)

    def process_help_command(self):
        """Prints the help text"""
        print(commands.HELP_TEXT)

    def process_quit_command(self, save_function: Callable[[str, List[CBT.CheckbookTransaction]], None]) -> None:
        """Quit the program. Save if necessary.

        Args:
            save_function (function): function used to save the checkbook
        """
        if self.checkbook.is_edited():
            self.process_save_command(save_function)

    def process_delete_command(self, *args: str) -> None:
        if not args:
            delete_trans = int(input("Which transaction do you want to delete? : "))
        else:
            delete_trans = int(args[0])

        trans = self.checkbook.find_transaction(delete_trans)
        self.checkbook.get_register().remove(trans)
        self.checkbook.edited = True

    def process_sort_command(self, checkbook: CB.Checkbook, *args: str) -> CB.Checkbook:
        if not args:
            checkbook.order_by("Num")
            sort_key = config.SORT_BY_KEY
        else:
            sort_key = args[0]

        checkbook.order_by(sort_key.capitalize())
        return checkbook

    def process_search_command(self, checkbook: CB.Checkbook, *args: str) -> CB.Checkbook:
        sub_book = CB.Checkbook()
        if not args:
            search_terms = input("Enter your search terms : ")
        else:
            search_terms = " ".join(args)
        trans_list = self._process_checkbook_sub_list(checkbook, "Desc", search_terms)
        sub_book.create_based_on_list(trans_list)
        return sub_book

    def process_print_command(self, checkbook: CB.Checkbook, *args: str) -> CB.Checkbook:
        sub_book = CB.Checkbook()
        trans_list = []
        if not args:
            trans_list = self._process_checkbook_sub_list(checkbook)
        elif len(args) == 2:
            trans_list = self._process_checkbook_sub_list(checkbook, *args)

        sub_book.create_based_on_list(trans_list)
        return sub_book

    def _process_checkbook_sub_list(self, checkbook: CB.Checkbook, *args: str) -> List[CBT.CheckbookTransaction]:
        transaction_list = []

        if not args:
            transaction_list = checkbook.get_register()
        elif len(args) == 2:
            transaction_list = checkbook.get_specific_list(*args)

        return transaction_list

    def process_resequence_command(self, checkbook: CB.Checkbook) -> None:
        sequenceNum = 1
        for cbt in checkbook.get_register():
            cbt.set_value("Num", sequenceNum)
            sequenceNum += 1

        self.checkbook.set_edited(True)