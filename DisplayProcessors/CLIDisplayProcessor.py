import locale

import CheckbookTransaction as CBT
from Constants import config
from Constants import printConstants as PC
from Exceptions import *
from datetime import datetime
from Constants import commands

ROW_SEP = '\n' + str((PC.HLINE_CHAR * (sum(PC.SIZE_LIST) + len(PC.SIZE_LIST)))) + '\n'


def _gen_header_print():
    """
    Creates the header line at the top of the register
    @return: pretty print for the checkbook register header
    """
    header = ROW_SEP
    header += PC.VLINE_CHAR
    for i in range(len(CBT.KEYS)):
        header_length = PC.SIZE_LIST[i]
        format_string = '{:^' + str(header_length) + '}'
        header += format_string.format(CBT.KEYS[i]) + PC.VLINE_CHAR
    return header

def _gen_transaction_print(transaction):
    string = PC.VLINE_CHAR
    for i in range(len(CBT.KEYS)):
        header_length = PC.SIZE_LIST[i]
        format_string = '{:^' + str(header_length) + '}'
        val = transaction.data.get(CBT.KEYS[i])
        if type(val) is datetime:
            val = datetime.strftime(transaction.data.get(CBT.KEYS[i]), config.DATE_FORMAT)
        elif type(val) is float:
            val = locale.currency(val, grouping=config.THOUSAND_SEP)
        string += format_string.format(str(val)) + PC.VLINE_CHAR
    return string
    

def _gen_all_transactions_print(transaction_list):
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


def _gen_total_line_print(total):
    """
    creates the total line at the bottom of the register
    @param total: the total value to print in the line
    @type total: float
    @return: pretty print of the given total for the checkbook register
    """
    string = PC.VLINE_CHAR
    # format total: text
    format_string = '{:>' + str(sum(PC.SIZE_LIST[:-2]) + 4) + '}'
    string += format_string.format("Total : ")
    # format amount
    format_string = '{:^' + str((PC.SIZE_LIST[-2])) + '}'
    string += format_string.format(locale.currency(total, grouping=config.THOUSAND_SEP))
    # format final bar
    format_string = '{:>' + str((PC.SIZE_LIST[-1]) + 2) + '}'
    string += format_string.format(PC.VLINE_CHAR)
    return string


def _get_total_for_list(transaction_list):
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


def print_checkbook(checkbook, *args):
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

    return output

class CLIRun:

    def __init__(self, command_processor, save_function, load_function):
        self.command_processor = command_processor
        self.save_function = save_function
        self.load_function = load_function

    def _handle_user_input(self):
        """Gather user input. If the input is empty, make it an empty string.
        Returns:
            inputVal (list) : list containing one or more strings
        """
        inputVal = input("What would you like to do? : ").strip().split()
        if len(inputVal) == 0:
            inputVal = [""]

        inputVal[0].lower()
        return inputVal

    def main(self):
        print("Welcome to your checkbook!")
        self.command_processor.process_print_command()
        quit = False
        while(not quit):
            try:
                val = self._handle_user_input()
                if(val[0] == commands.HELP_COMMAND):
                    self.command_processor.process_help_command()
                elif(val[0] == commands.PRINT_COMMAND):
                    self.command_processor.process_print_command(*val[1:])
                elif(val[0] == commands.ADD_COMMAND):
                    self.command_processor.process_add_command()
                elif(val[0] == commands.EDIT_COMMAND):
                    self.command_processor.process_edit_command(*val[1:])
                elif(val[0] == commands.REPORT_COMMAND):
                    self.command_processor.process_report_command()
                elif(val[0] == commands.LOAD_COMMAND):
                    self.command_processor.process_save_command(self.save_function)
                    self.command_processor.process_load_command(self.load_function, *val[1:])
                    self.command_processor.process_print_command()
                elif(val[0] == commands.SAVE_COMMAND):
                    self.command_processor.process_save_command(self.save_function)
                elif(val[0] == commands.DELETE_COMMAND):
                    self.command_processor.process_delete_command(*val[1:])
                elif(val[0] in commands.EXIT_LIST):
                    self.command_processor.process_quit_command(self.save_function)
                    quit = True
                elif (val[0] == commands.SORT_COMMAND):
                    self.command_processor.process_sort_command(*val[1:])
                    self.command_processor.process_print_command()
                elif (val[0] == commands.SEARCH_COMMAND):
                    self.command_processor.process_search_command(*val[1:])
                    
            except InvalidDateError as date_error:
                print(date_error)
            except:
                pass
