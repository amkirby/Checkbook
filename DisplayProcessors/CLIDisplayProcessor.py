import locale
from datetime import datetime
from typing import Callable, List

import CheckbookTransaction as CBT
import ConfigurationProcessor as Conf
import copyToAnother as CTA
from Checkbook import Checkbook
from CommandProcessor import CommandProcessor
from Constants import commands
from Exceptions import *

conf = Conf.ConfigurationProcessor()

ROW_SEP = '\n' + str((conf.get_property("HLINE_CHAR") * (sum(conf.get_property("SIZE_LIST")) + len(conf.get_property("SIZE_LIST"))))) + '\n'


def _gen_header_print() -> str:
    """
    Creates the header line at the top of the register
    @return: pretty print for the checkbook register header
    """
    header = ROW_SEP
    header += conf.get_property("VLINE_CHAR")
    for i in range(len(CBT.KEYS)):
        header_length = conf.get_property("SIZE_LIST")[i]
        format_string = '{:^' + str(header_length) + '}'
        header += format_string.format(CBT.KEYS[i]) + conf.get_property("VLINE_CHAR")
    return header

def _gen_transaction_print(transaction: CBT.CheckbookTransaction) -> str:
    string = conf.get_property("VLINE_CHAR")
    for i in range(len(CBT.KEYS)):
        header_length = conf.get_property("SIZE_LIST")[i]
        format_string = '{:^' + str(header_length) + '}'
        val = transaction.data.get(CBT.KEYS[i])
        if type(val) is datetime:
            val = datetime.strftime(transaction.get_value(CBT.KEYS[i]), conf.get_property("DATE_FORMAT")) #transaction.data.get(CBT.KEYS[i])
        elif type(val) is float:
            val = locale.currency(val, grouping=conf.get_property("THOUSAND_SEP"))
        string += format_string.format(str(val)) + conf.get_property("VLINE_CHAR")
    return string
    

def _gen_all_transactions_print(transaction_list: List[CBT.CheckbookTransaction]) -> str:
    """
    Creates the print for each transaction in the register

    @param transaction_list: the list of CBTs to loop through to generate
                             the transaction print. If None, loop through
                             the whole checkbook
    @return: pretty print for the given transaction list
    """
    string = ''
    for elem in transaction_list:
        string += _gen_transaction_print(elem)
        string += ROW_SEP
    return string


def _gen_total_line_print(total: float) -> str:
    """
    creates the total line at the bottom of the register
    @param total: the total value to print in the line
    @type total: float
    @return: pretty print of the given total for the checkbook register
    """
    string = conf.get_property("VLINE_CHAR")
    # format total: text
    format_string = '{:>' + str(sum(conf.get_property("SIZE_LIST")[:-2]) + 4) + '}'
    string += format_string.format("Total : ")
    # format amount
    format_string = '{:^' + str((conf.get_property("SIZE_LIST")[-2])) + '}'
    string += format_string.format(locale.currency(total, grouping=conf.get_property("THOUSAND_SEP")))
    # format final bar
    format_string = '{:>' + str((conf.get_property("SIZE_LIST")[-1]) + 2) + '}'
    string += format_string.format(conf.get_property("VLINE_CHAR"))
    return string


def _get_total_for_list(transaction_list: List[CBT.CheckbookTransaction]) -> float:
    """

    @param transaction_list: the list of CBTs to loop through to generate
                             the transaction print. If None, loop through
                             the whole checkbook
    @return: the total value for the given transaction list
    """
    total = 0.0
    for current_cbt in transaction_list:
        total += current_cbt.get_amount()

    return total


def print_checkbook(checkbook: Checkbook, *args: str) -> None:
    """
    pretty print the given checkbook
    @param checkbook: the checkbook being processed
    @type checkbook: Checkbook
    @param args: an optional key, value pair for specific print
    @return: pretty print of the checkbook register
    """
    transaction_list = []
    total = 0.0
    if not args:
        transaction_list = checkbook.get_register()
    elif len(args) == 2:
        transaction_list = checkbook.get_specific_list(*args)

    total = _get_total_for_list(transaction_list)
    output = _gen_header_print()
    output += ROW_SEP
    output += _gen_all_transactions_print(transaction_list)
    output += _gen_total_line_print(total)
    output += ROW_SEP

    print(output)

class CLIRun:

    def __init__(self, command_processor:CommandProcessor, save_function: Callable[[str, List[CBT.CheckbookTransaction]], None], load_function: Callable[[str], List[CBT.CheckbookTransaction]]):
        self.command_processor = command_processor
        self.save_function = save_function
        self.load_function = load_function

    def _handle_user_input(self) -> List[List[str]]:
        """Gather user input. If the input is empty, make it an empty string.
        Returns:
            inputVal (list) : list containing one or more strings
        """
        inputVal: List[List[str]] = []
        commands = input("What would you like to do? : ").strip().split("|")
        for command in commands:
            inputVal.append(command.strip().split(" ", 2))

        return inputVal

    def main(self):
        print("Welcome to your checkbook!")
        checkbook = self.command_processor.checkbook
        self.command_processor.process_print_command(checkbook)
        print_checkbook(checkbook)
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
                        checkbook = self.command_processor.checkbook
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
                        CTA.copy(self.command_processor.checkbook.get_file_name(), conf.get_property("DEFAULT_COPY_TO"))
                    else:
                        error = InvalidCommandError(val[0], "Invalid command entered : ")
                        raise error
                        
                if(needs_to_print):
                    print_checkbook(checkbook)
                    needs_to_print = False
                    checkbook = self.command_processor.checkbook
            except InvalidDateError as date_error:
                print(date_error)
            except InvalidDateRangeError as month_error:
                print(month_error)
            except InvalidCommandError as command_error:
                print(command_error)
            except Exception as e:
                print(e)
