from DisplayProcessors import CLIDisplayProcessor
import CheckbookTransaction as CBT
import checkbookReport as CR
from Constants import commands
from Constants import config


def _apply_debit_multiplier(debit_transaction):
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

    def __init__(self, checkbook):
        """Initializes the checkbook that will be used for the operations

        Args:
            checkbook (Checkbook) : the checkbook to operate on
        """
        self.checkbook = checkbook

    def process_command(self, function, *args):
        """Performs the effects of the specified function on the checkbook

        Args:
            function (function) : A function that takes a checkbook and performs
                                  some action
            args (variable args) : optional arguments that can be passed to the specified
                                   function
        """
        function(self.checkbook, *args)

    def _do_save(self, save_function):
        """Saves the checkbook

        Args:
            save_function (function): function used to save the checkbook
        """
        save = input("Would you like to save? (y or n) ")
        if save.lower() == "y":
            self.checkbook.save(save_function)
            print("save successful!")

    def _select_with_number(self, text_list, key, def_text=None):
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

    def process_add_command(self):
        """Adds a transaction to the checkbook"""
        print("Enter your transaction")
        cbt = CBT.CheckbookTransaction()
        for key in CBT.KEYS:
            if key != "Num":
                if key == "Category":
                    val = self._select_with_number(config.CATEGORIES, key)
                elif key == "Trans":
                    val = self._select_with_number(commands.TRANS_TYPES, key)
                else:
                    val = input(key + " : ")

                cbt.set_value(key, val.capitalize())

        _apply_debit_multiplier(cbt)
        self.checkbook.add_single_trans(cbt)

    def process_edit_command(self, *args):
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
                    val = self._select_with_number(config.CATEGORIES, key, trans.get_value(key))
                elif key == "Trans":
                    val = self._select_with_number(commands.TRANS_TYPES, key, trans.get_value(key))
                else:
                    val = input(key + " (" + str(trans.get_value(key)) + ")" + " : ")
                if val.strip() != "":
                    trans.set_value(key, val.capitalize())
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

    def process_load_command(self, load_function, *args):
        """Load another checkbook

        Args:
            load_function (function): function used to save the checkbook
            *args (variable args)   : Can specify the checkbook to load
        """

        if not args:
            file_name = input("Enter an XML file to load : ")
        else:
            file_name = args[0]
        self.checkbook.clear()
        self.checkbook.load(file_name, load_function)

    def process_save_command(self, save_function):
        """Save the checkbook

        Args:
            save_function (function): function used to save the checkbook
        """
        if self.checkbook.is_edited():
            self._do_save(save_function)

    def process_help_command(self):
        """Prints the help text"""
        print(commands.HELP_TEXT)

    def process_quit_command(self, save_function):
        """Quit the program. Save if necessary.

        Args:
            save_function (function): function used to save the checkbook
        """
        if self.checkbook.is_edited():
            self.process_save_command(save_function)

    def process_delete_command(self, *args):
        if not args:
            delete_trans = int(input("Which transaction do you want to delete? : "))
        else:
            delete_trans = int(args[0])

        trans = self.checkbook.find_transaction(delete_trans)
        self.checkbook.get_register().remove(trans)

    def process_sort_command(self, *args):
        if not args:
            self.checkbook.order_by("Num")
            sort_key = config.SORT_BY_KEY
        else:
            sort_key = args[0]
        
        self.checkbook.order_by(sort_key)

    def process_print_command(self, *args):
        """Prints the checkbook

        Args:
            *args (variable args): can specify what to print
        """
        if not args:
            print(CLIDisplayProcessor.print_checkbook(self.checkbook))
        elif len(args) == 2:
            print(CLIDisplayProcessor.print_checkbook(self.checkbook, *args))
        else:
            print_help_text = """
Usage : print [<key> <value> | <help>]
Possible keys with their values :
    Date     : a number to represent the month
    Trans    : {}
    Category : {}
help displays this text
            """
            print(print_help_text.format(", ".join(s for s in commands.TRANS_TYPES),
                                         ", ".join(s for s in config.CATEGORIES)))
