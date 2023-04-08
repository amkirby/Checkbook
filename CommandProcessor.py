import string
from typing import Any, Callable, List, Optional

import Checkbook as CB
import checkbookReport as CR
import CheckbookTransaction as CBT
import ConfigurationProcessor as Conf
from Constants import commands
from Exceptions import *
from DisplayProcessors import CLIDisplayProcessor as CDP
from Tools import copyToAnother as CTA
from Tools import SaveToCSV as STC
from Tools import FindMissingTransactions as COMP

conf = Conf.ConfigurationProcessor()


def _apply_debit_multiplier(debit_transaction: CBT.CheckbookTransaction) -> None:
    if((debit_transaction.is_debit() and int(debit_transaction.get_amount()) > 0)
        or (not debit_transaction.is_debit() and int(debit_transaction.get_amount()) < 0)):
        debit_transaction.set_value("Amount", debit_transaction.get_amount() * conf.get_property("DEBIT_MULTIPLIER"))

class CommandProcessor:
    """A class to process commands entered by the user. A function should be
    passed to each method to do the actual processing.
    ****NOTE: Each passed function is expected to take a Checkbook object as a parameter.
    ****NOTE: The separate methods remain to facilitate inheritance if desired.

    Attributes:
        checkbook (Checkbook) : the current checkbook the user is using
    """

    def __init__(self, checkbook: CB.Checkbook, display_processor :CDP.CLIDisplayProcessor):
        """Initializes the checkbook that will be used for the operations

        Args:
            checkbook (Checkbook) : the checkbook to operate on
        """
        self.checkbook = checkbook
        self._trans_selection = ""
        self.display_processor :CDP.CLIDisplayProcessor = display_processor

    def confirm_selection(self, command: str) -> bool:
        confirmed = True

        user_input = self.display_processor.handle_single_input("Would you like to " + command + "? (Y or n) ")
        if user_input.lower() == "n":
            confirmed = False


        return confirmed

    def _do_save(self, save_function: Callable[[str, List[CBT.CheckbookTransaction]], None]) -> None:
        """Saves the checkbook

        Args:
            save_function (function): function used to save the checkbook
        """
        if(self.confirm_selection("save")):
            self.checkbook.save(save_function)
            self.display_processor.display_message("save successful!")


    def _handle_edit_description(self, current_desc: str) -> str:
        edit_val = current_desc
        user_input = self.display_processor.handle_single_input("Desc (" + current_desc + ")(- to prepend, + to append) : ").strip()
        if(user_input.startswith("-")):
            user_input = user_input[1:]
            edit_val = user_input.strip() + " " + current_desc
        elif(user_input.startswith("+")):
            user_input = user_input[1:]
            edit_val = current_desc + " " + user_input.strip()
        elif(user_input.strip() != ""):
            edit_val = user_input.strip()


        return edit_val

    def process_add_command(self) -> None:
        """Adds a transaction to the checkbook"""
        self.display_processor.display_message("Enter your transaction")
        cbt = CBT.CheckbookTransaction()
        val = ""
        try:
            for key in CBT.KEYS:
                if key != "Num":
                    if key == "Category":
                        val = self.display_processor.select_from_list(conf.get_property("CATEGORIES_FOR_ADD")[self._trans_selection], key)
                    elif key == "Trans":
                        val = self.display_processor.select_from_list(commands.TRANS_TYPES, key)
                        self._trans_selection = val if val in commands.TRANS_TYPES else "all"
                    else:
                        val = self.display_processor.handle_single_input(key + " : ")

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
            transactions_to_edit = self._process_list_input(self.display_processor.handle_single_input("Which transaction(s) do you want to edit? : "))
        else:
            transactions_to_edit = self._process_list_input(args[0])

        transactions_from_cb = self.checkbook.find_transactions(transactions_to_edit)
        self.display_processor.print_list_of_trans(" Transaction(s) Being Edited ", conf.get_property("MAX_WIDTH"), conf.get_property("TRANS_FILL_CHAR"), transactions_from_cb)
        if(transactions_from_cb is not None and self.confirm_selection("edit")):
            for trans in transactions_from_cb:
                self.display_processor.print_list_of_trans(" Current Transaction Being Edited ", conf.get_property("MAX_WIDTH"), conf.get_property("TRANS_FILL_CHAR"), [trans])
                for key in CBT.KEYS:
                    if key != "Num":
                        if key == "Category":
                            val = self.display_processor.select_from_list(conf.get_property("CATEGORIES_FOR_ADD")[self._trans_selection], key, trans.get_value(key))
                        elif key == "Trans":
                            val = self.display_processor.select_from_list(commands.TRANS_TYPES, key, trans.get_value(key))
                            self._trans_selection = val if val.strip() != "" else trans.get_value(key)
                        elif key == "Desc":
                            val = self._handle_edit_description(trans.get_value("Desc"))
                        else:
                            val = self.display_processor.handle_single_input(key + " (" + str(trans.get_value(key)) + ")" + " : ")
                        if val.strip() != "":
                            trans.set_value(key, string.capwords(val))
                            self.checkbook.set_edited(True)

                _apply_debit_multiplier(trans)

    def process_report_command(self):
        """Generate a report"""
        format_string = "{:<" + str(CR.MAX_REPORT_TYPE) + "}"
        date_range = None
        self.display_processor.display_message("Report Types:")
        for i in range(len(CR.REPORT_TYPES)):
            self.display_processor.display_message(format_string.format(CR.REPORT_TYPES[i]), ": " + str(i))
        rep_type = int(self.display_processor.handle_single_input("Enter desired report number : "))
        cr = CR.CheckbookReport(self.checkbook)
        rep_method = CR.CheckbookReport.dispatcher[CR.REPORT_TYPES[rep_type]]
        if rep_type == 0:
            date_range = self.display_processor.handle_single_input("Enter desired date criteria : ")

        report_text = rep_method(cr, date_range)
        self.display_processor.display_message(report_text)

    def process_load_command(self, load_function: Callable[[str], List[CBT.CheckbookTransaction]], *args: str) -> None:
        """Load another checkbook

        Args:
            load_function (function): function used to save the checkbook
            *args (variable args)   : Can specify the checkbook to load
        """
        file_name: str = ""
        if not args:
            file_name = self.display_processor.handle_single_input("Enter an XML file to load : ")
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
        self.display_processor.display_message(commands.HELP_TEXT)

    def process_quit_command(self, save_function: Callable[[str, List[CBT.CheckbookTransaction]], None]) -> None:
        """Quit the program. Save if necessary.

        Args:
            save_function (function): function used to save the checkbook
        """
        if self.checkbook.is_edited():
            self.process_save_command(save_function)

    def process_delete_command_old(self, *args: str) -> None:
        if not args:
            delete_trans = int(self.display_processor.handle_single_input("Which transaction do you want to delete? : "))
        else:
            delete_trans = int(args[0])

        trans = self.checkbook.find_transaction(delete_trans)
        self.display_processor.print_list_of_trans(" Transaction Being Deleted ", conf.get_property("MAX_WIDTH"), conf.get_property("TRANS_FILL_CHAR"), [trans])
        if(trans is not None and self.confirm_selection("delete")):
            self.checkbook.delete_transaction(trans)

    def process_delete_command(self, *args: str) -> None:
        if not args:
            transactions_to_delete = self._process_list_input(self.display_processor.handle_single_input("Which transaction(s) do you want to delete? : "))
        else:
            transactions_to_delete = self._process_list_input(args[0])

        transactions_from_cb = self.checkbook.find_transactions(transactions_to_delete)
        self.display_processor.print_list_of_trans(" Transaction Being Deleted ", conf.get_property("MAX_WIDTH"), conf.get_property("TRANS_FILL_CHAR"), transactions_from_cb)
        if(transactions_from_cb is not None and self.confirm_selection("delete")):
            self.checkbook.delete_transactions(transactions_from_cb)

    def process_sort_command(self, checkbook: CB.Checkbook, *args: str) -> CB.Checkbook:
        if not args:
            checkbook.order_by("Num")
            sort_key = conf.get_property("SORT_BY_KEY")
        else:
            sort_key = args[0]

        checkbook.order_by(sort_key.capitalize())
        return checkbook

    def process_search_command(self, checkbook: CB.Checkbook, *args: str) -> CB.Checkbook:
        sub_book = CB.Checkbook()
        if not args:
            search_terms = self.display_processor.handle_single_input("Enter your search terms : ")
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
        if(self.confirm_selection("resequence")):
            sequenceNum = 1
            for cbt in checkbook.get_register():
                cbt.set_value("Num", sequenceNum)
                sequenceNum += 1
            CBT.CheckbookTransaction.set_uid(sequenceNum)
            self.checkbook.set_edited(True)
            self.display_processor.display_message("resequence successful!")

    def _process_list_input(self, val: str) -> List[str]:
        return_val = [""]

        if(val is not None):
            return_val = [x.strip() for x in val.split(",")]

        return return_val



class CLIRun:

    def __init__(self, command_processor:CommandProcessor, display_processor:CDP.CLIDisplayProcessor, save_function: Callable[[str, List[CBT.CheckbookTransaction]], None], load_function: Callable[[str], List[CBT.CheckbookTransaction]]):
        self.command_processor = command_processor
        self.display_processor = display_processor
        self.save_function = save_function
        self.load_function = load_function
        self.checkbook = self.command_processor.checkbook

    def _handle_user_input(self) -> List[List[str]]:
        """Gather user input. If the input is empty, make it an empty string.
        Returns:
            inputVal (list) : list containing one or more strings
        """
        inputVal: List[List[str]] = []
        commands = self.display_processor.handle_single_input("What would you like to do? : ").strip().split("|")
        for command in commands:
            inputVal.append(command.strip().split(" ", 2))

        return inputVal

    def main(self):
        self.display_processor.display_message("Welcome to your checkbook!")
        checkbook = self.checkbook
        self.command_processor.process_print_command(checkbook)
        self.display_processor.display_checkbook(checkbook)
        quit = False
        needs_to_print = False
        while(not quit):
            try:
                all_val = self._handle_user_input()
                for val in all_val:
                    if(val[0] == commands.HELP_COMMAND):
                        self.command_processor.process_help_command()
                    elif(val[0] == commands.PRINT_COMMAND):
                            checkbook = self.command_processor.process_print_command(checkbook, *val[1:])
                            needs_to_print = True
                    elif(val[0] == commands.ADD_COMMAND):
                        self.command_processor.process_add_command()
                    elif(val[0] == commands.EDIT_COMMAND):
                        self.command_processor.process_edit_command(*val[1:])
                    elif(val[0] == commands.REPORT_COMMAND):
                        self.command_processor.process_report_command()
                    elif(val[0] == commands.LOAD_COMMAND):
                        self.command_processor.process_save_command(self.save_function)
                        self.command_processor.process_load_command(self.load_function, *val[1:])
                        checkbook = self.checkbook
                        needs_to_print = True
                    elif(val[0] == commands.SAVE_COMMAND):
                        self.command_processor.process_save_command(self.save_function)
                    elif(val[0] == commands.DELETE_COMMAND):
                        self.command_processor.process_delete_command(*val[1:])
                    elif(val[0] in commands.EXIT_LIST):
                        self.command_processor.process_quit_command(self.save_function)
                        quit = True
                    elif (val[0] == commands.SORT_COMMAND):
                        checkbook = self.command_processor.process_sort_command(checkbook, *val[1:])
                        needs_to_print = True
                    elif (val[0] == commands.SEARCH_COMMAND):
                        checkbook = self.command_processor.process_search_command(checkbook, *val[1:])
                        needs_to_print = True
                    elif (val[0] == commands.RESEQUENCE_COMMAND):
                        self.command_processor.process_resequence_command(checkbook)
                        needs_to_print = True
                    elif (val[0] == commands.COPY_COMMAND):
                        CTA.copy(self.checkbook.get_file_name(), conf.get_property("DEFAULT_COPY_TO"))
                    elif(val[0] == commands.CSV_COMMAND):
                        STC.save_to_csv(self.checkbook.get_file_name())
                    elif(val[0] == commands.COMPARE_COMMAND):
                        checkbook = COMP.process_compare()
                        needs_to_print = True
                    else:
                        error = InvalidCommandError(val[0], "Invalid command entered : ")
                        raise error
                        
                if(needs_to_print):
                    self.display_processor.display_checkbook(checkbook)
                    needs_to_print = False
                    checkbook = self.checkbook
            except InvalidDateError as date_error:
                print(date_error)
            except InvalidDateRangeError as month_error:
                print(month_error)
            except InvalidCommandError as command_error:
                print(command_error)
            except Exception as e:
                print(e)
