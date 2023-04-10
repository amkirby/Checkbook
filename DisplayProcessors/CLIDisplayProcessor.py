import locale
from datetime import datetime
import textwrap
from typing import Any, Dict, List, Optional

import CheckbookTransaction as CBT
import ConfigurationProcessor as Conf
from Checkbook import Checkbook
from Exceptions import *

conf = Conf.ConfigurationProcessor()

ROW_SEP = '\n' + str((conf.get_property("HLINE_CHAR") * (sum(conf.get_property("SIZE_LIST")) + len(conf.get_property("SIZE_LIST"))))) + '\n'

def _build_template():
    template = ""
    template += conf.get_property("VLINE_CHAR")
    for i in range(len(CBT.KEYS)):
        header_length = conf.get_property("SIZE_LIST")[i]
        format_string = '{' + CBT.KEYS[i] + ':^' + str(header_length) + '}'
        template += format_string + conf.get_property("VLINE_CHAR")


    return template

TRANSACTION_ROW_PRINT_TEMPLATE = _build_template()

class CLIDisplayProcessor:
    def __init__(self):
        pass



    def _gen_header_print(self) -> str:
        """
        Creates the header line at the top of the register
        @return: pretty print for the checkbook register header
        """
        header = ROW_SEP

        vals = {}
        for i in range(len(CBT.KEYS)):
            vals[CBT.KEYS[i]] = CBT.KEYS[i]

        header += TRANSACTION_ROW_PRINT_TEMPLATE.format(**vals)
        return header

    # def _any_keys_need_wrapped(transaction_vals) -> bool:
    #     needs_wrapped = False
    #     for i in range(len(CBT.KEYS)):
    #         if len(transaction_vals[CBT.KEYS[i]]) > conf.get_property("SIZE_LIST")[i]:
    #             needs_wrapped = True
    #             break
        
    #     return needs_wrapped

    def _create_default_row(self) -> Dict[str, str]:
        default_row :Dict[str, str] = {}
        for key in CBT.KEYS:
            default_row[key] = ""

        return default_row

    def _get_row_for_index(self, rows_to_create  :List[Dict[str, str]], index :int) -> Dict[str, str]:
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
        wrapped_text :str = ""
        rows_to_create :List[Dict[str, str]] = []

        for i in range(len(CBT.KEYS)):
            text_after_wrap = textwrap.fill(transaction_vals[CBT.KEYS[i]], width=conf.get_property("SIZE_LIST")[i]).split("\n")
            self._fill_in_rows(rows_to_create, CBT.KEYS[i], text_after_wrap)

        for row in rows_to_create:
            wrapped_text += TRANSACTION_ROW_PRINT_TEMPLATE.format(**row) + "\n"


        return wrapped_text.strip()

    def _gen_transaction_print(self, transaction: CBT.CheckbookTransaction) -> str:
        string = ""
        transaction_vals = {}
        for i in range(len(CBT.KEYS)):
            val = transaction.data.get(CBT.KEYS[i])
            if type(val) is datetime:
                val = datetime.strftime(transaction.get_value(CBT.KEYS[i]), conf.get_property("DATE_FORMAT"))
            elif type(val) is float:
                val = locale.currency(val, grouping=conf.get_property("THOUSAND_SEP"))

            transaction_vals[CBT.KEYS[i]] = str(val)
            
        string += self._wrap_transaction_text(transaction_vals) #TRANSACTION_ROW_PRINT_TEMPLATE.format(**vals)
            
        return string
        

    def _gen_all_transactions_print(self, transaction_list: List[CBT.CheckbookTransaction]) -> str:
        """
        Creates the print for each transaction in the register

        @param transaction_list: the list of CBTs to loop through to generate
                                the transaction print. If None, loop through
                                the whole checkbook
        @return: pretty print for the given transaction list
        """
        string = ''
        for elem in transaction_list:
            string += self._gen_transaction_print(elem)
            string += ROW_SEP
        return string


    def _gen_total_line_print(self, total: float) -> str:
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


    def _get_total_for_list(self, transaction_list: List[CBT.CheckbookTransaction]) -> float:
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


    def print_checkbook(self, checkbook: Checkbook, *args: str) -> None:
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

        total = self._get_total_for_list(transaction_list)
        output = self._gen_header_print()
        output += ROW_SEP
        output += self._gen_all_transactions_print(transaction_list)
        output += self._gen_total_line_print(total)
        output += ROW_SEP

        print(output)

    def display_checkbook(self, checkbook :Checkbook):
        self.print_checkbook(checkbook)

    def display_message(self, message :str):
        print(message)

    def handle_single_input(self, input_message :str):
        return input(input_message)

    def print_list_of_trans(self, header_text : str, width : int, fill_char : str, list_of_trans : List[CBT.CheckbookTransaction]):
        header_line = header_text.center(width,fill_char)
        print(header_line)
        for current_trans in list_of_trans:
            # if(current_trans != None):
            print(current_trans)
        print(fill_char * len(header_line))

    def select_from_list(self, text_list: List[str], key: str, def_text: Optional[Any]=None) -> str:
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
            self.display_message("  " + format_string.format(text_list[i]) + " " + str(i))
        val = self.handle_single_input(key + prev_text + " : ")
        if val.strip() != "" and val.isdigit() and (0 <= int(val) < len(text_list)):
            val = text_list[int(val)]
        return val


# class CLIRun:

#     def __init__(self, command_processor:CommandProcessor, save_function: Callable[[str, List[CBT.CheckbookTransaction]], None], load_function: Callable[[str], List[CBT.CheckbookTransaction]]):
#         self.command_processor = command_processor
#         self.save_function = save_function
#         self.load_function = load_function

#     def _handle_user_input(self) -> List[List[str]]:
#         """Gather user input. If the input is empty, make it an empty string.
#         Returns:
#             inputVal (list) : list containing one or more strings
#         """
#         inputVal: List[List[str]] = []
#         commands = input("What would you like to do? : ").strip().split("|")
#         for command in commands:
#             inputVal.append(command.strip().split(" ", 2))

#         return inputVal

#     def main(self):
#         print("Welcome to your checkbook!")
#         checkbook = self.command_processor.checkbook
#         self.command_processor.process_print_command(checkbook)
#         print_checkbook(checkbook)
#         quit = False
#         needs_to_print = False
#         while(not quit):
#             try:
#                 all_val = self._handle_user_input()
#                 for val in all_val:
#                     if(val[0] == commands.HELP_COMMAND):
#                         self.command_processor.process_help_command()
#                     elif(val[0] == commands.PRINT_COMMAND):
#                             checkbook = self.command_processor.process_print_command(checkbook, *val[1:])
#                             needs_to_print = True
#                     elif(val[0] == commands.ADD_COMMAND):
#                         self.command_processor.process_add_command()
#                     elif(val[0] == commands.EDIT_COMMAND):
#                         self.command_processor.process_edit_command(*val[1:])
#                     elif(val[0] == commands.REPORT_COMMAND):
#                         self.command_processor.process_report_command()
#                     elif(val[0] == commands.LOAD_COMMAND):
#                         self.command_processor.process_save_command(self.save_function)
#                         self.command_processor.process_load_command(self.load_function, *val[1:])
#                         checkbook = self.command_processor.checkbook
#                         needs_to_print = True
#                     elif(val[0] == commands.SAVE_COMMAND):
#                         self.command_processor.process_save_command(self.save_function)
#                     elif(val[0] == commands.DELETE_COMMAND):
#                         self.command_processor.process_delete_command(*val[1:])
#                     elif(val[0] in commands.EXIT_LIST):
#                         self.command_processor.process_quit_command(self.save_function)
#                         quit = True
#                     elif (val[0] == commands.SORT_COMMAND):
#                         checkbook = self.command_processor.process_sort_command(checkbook, *val[1:])
#                         needs_to_print = True
#                     elif (val[0] == commands.SEARCH_COMMAND):
#                         checkbook = self.command_processor.process_search_command(checkbook, *val[1:])
#                         needs_to_print = True
#                     elif (val[0] == commands.RESEQUENCE_COMMAND):
#                         self.command_processor.process_resequence_command(checkbook)
#                         needs_to_print = True
#                     elif (val[0] == commands.COPY_COMMAND):
#                         CTA.copy(self.command_processor.checkbook.get_file_name(), conf.get_property("DEFAULT_COPY_TO"))
#                     elif(val[0] == commands.CSV_COMMAND):
#                         STC.save_to_csv(self.command_processor.checkbook.get_file_name())
#                     elif(val[0] == commands.COMPARE_COMMAND):
#                         checkbook = COMP.process_compare()
#                         needs_to_print = True
#                     else:
#                         error = InvalidCommandError(val[0], "Invalid command entered : ")
#                         raise error
                        
#                 if(needs_to_print):
#                     print_checkbook(checkbook)
#                     needs_to_print = False
#                     checkbook = self.command_processor.checkbook
#             except InvalidDateError as date_error:
#                 print(date_error)
#             except InvalidDateRangeError as month_error:
#                 print(month_error)
#             except InvalidCommandError as command_error:
#                 print(command_error)
#             except Exception as e:
#                 print(e)
