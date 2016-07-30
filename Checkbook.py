import locale
from Constants import printConstants as PC
from Constants import config
import CheckbookTransaction as CBT

ROW_SEP = '\n' + (PC.HLINE_CHAR * (sum(PC.SIZE_LIST) + len(PC.SIZE_LIST))) + '\n'


class Checkbook:
    """A class that represents a checkbook

    Attributes:
        check_register (list) : contains instances of CheckbookTransaction
    """

    def __init__(self):
        """Initializes an empty check register"""
        self.check_register = []
        self.file_name = config.FILE_NAME
        self.edited = False

    def add(self, cbt_list):
        """Adds the specified list to the checkbook

        Parameter:
            cbt_list (list) : contains values in the order of the CBT.KEYS that
                             are used to create a transaction
        """
        cbt = CBT.CheckbookTransaction()
        for i in range(len(cbt_list)):
            cbt.set_value(CBT.KEYS[i], cbt_list[i])
        self.check_register.append(cbt)
        self.edited = True

    def add_single_trans(self, cbt):
        """Adds a CheckbookTransaction to the register

        Parameter:
             cbt (CheckbookTransaction) : the CBT to be added to the checkbook
        """
        self.check_register.append(cbt)
        self.edited = True

    def load(self, file_name, load_function):
        """Tries to load the specified file name into the check register

        Parameter:
            file_name (string) : the file to load into the checkbook
        """
        self.file_name = file_name
        self.check_register = load_function(self.file_name)

    def clear(self):
        """Clears the checkbook"""
        del self.check_register[:]
        CBT.CheckbookTransaction.reset_uid()

    def save(self, save_function):
        """Saves the checkbook in XML format"""
        save_function(self.file_name, self.check_register)
        self.edited = False

    def is_edited(self):
        """Returns if the checkbook has been edited"""
        return self.edited

    def set_edited(self, edit):
        """Sets the edited status to the specified value

        Parameter:
            edit (boolean) : the state to set if the checkbook is edited
        """
        self.edited = edit

    def get_transaction_type(self, trans_type):
        """Gets all transactions with the specified trans type

        Parameter:
            trans_type (string) : the transaction type to gather
        """
        return_list = []
        for elem in self.check_register:
            if elem.getDictionary().get("Trans") == trans_type:
                return_list.append(elem)
        return return_list

    def get_category(self, cat):
        """Gets all transactions with the specified category

        Parameter:
            cat (string) : the category to gather
        """
        return_list = []
        for elem in self.check_register:
            if elem.getDictionary().get("Category") == cat:
                return_list.append(elem)
        return return_list

    def get_month(self, find_month):
        """Gets all transactions with the specified month

        Parameter:
            find_month (int) : the integer value for the month to gather
        """
        month = find_month
        if type(month) is not int:
            month = int(month)

        return_list = []
        for elem in self.check_register:
            date = elem.getDictionary().get("Date")
            if date.month == month:
                return_list.append(elem)
        return return_list

    def get_total_for_trans(self, trans):
        """Get the total amount for the specified trans type

        Parameter:
            trans (string) : the transaction type that is totaled
        """
        trans_list = self.get_transaction_type(trans)
        total = 0.0
        for elem in trans_list:
            total += elem.getAmount()
        return total

    def get_total_for_trans_month(self, trans, month):
        """Get the total for the specified transaction in the specified month

        Parameters:
            trans (string) : the transaction type to total
            month (int)    : the month to total the trans type
        """
        month_list = self.get_month(month)
        total = 0.0
        for elem in month_list:
            if elem.getValue("Trans") == trans:
                total += elem.getAmount()
        return total

    def get_total_for_cat(self, category):
        """Get the total for the specified category

        Parameter:
            category (string) : The category to total
        """
        cat_list = self.get_category(category)
        total = 0.0
        for elem in cat_list:
            total += elem.getAmount()
        return total

    def get_total_for_cat_month(self, cat, month):
        """Get the total for the specified transaction in the specified month

        Parameters:
            cat (string) : the category to total
            month (int)  : the month to total the trans type
        """
        month_list = self.get_month(month)
        total = 0.0
        for elem in month_list:
            if elem.getValue("Category") == cat:
                total += elem.getAmount()
        return total

    def get_total(self):
        """Gets the total for the register"""
        total = 0.0
        for elem in self.check_register:
            total += elem.getAmount()
        return total

    def get_month_total(self, month):
        """Gets the total for the specified month

        Parameter:
            month (int) : the month to total
        """
        month_list = self.get_month(month)
        total = 0.0
        for elem in month_list:
            total += elem.getAmount()
        return total

    def find_transaction(self, in_trans):
        """Gets the specified transaction number from the register

        Parameter:
            in_trans (int) : the transaction to gather
        """
        return self.check_register[in_trans - 1]

    def _gen_total_line_print(self):
        """creates the total line at the bottom of the register"""
        string = PC.VLINE_CHAR
        # format total: text
        format_string = '{:>' + str(sum(PC.SIZE_LIST[:-2]) + 4) + '}'
        string += format_string.format("Total : ")
        # format amount
        format_string = '{:^' + str((PC.SIZE_LIST[-2])) + '}'
        string += format_string.format(locale.currency(self.get_total(), grouping=config.THOUSAND_SEP))
        # format final bar
        format_string = '{:>' + str((PC.SIZE_LIST[-1]) + 2) + '}'
        string += format_string.format(PC.VLINE_CHAR)
        return string

    def _gen_header_print(self):
        """Creates the header line at the top of the register"""
        header = ROW_SEP
        header += PC.VLINE_CHAR
        for i in range(len(CBT.KEYS)):
            header_length = PC.SIZE_LIST[i]
            format_string = '{:^' + str(header_length) + '}'
            header += format_string.format(CBT.KEYS[i]) + PC.VLINE_CHAR
        return header

    def _gen_trans_print(self, print_list=None):
        """Creates the print for each transaction in the register

        Parameter:
            print_list (list) : the list of CBTs to loop through to generate
                               the transaction print. If None, loop through 
                               the whole checkbook
        """
        iter_list = print_list
        if iter_list is None:
            iter_list = self.check_register

        string = ''
        for elem in iter_list:
            string += str(elem)
            string += ROW_SEP
        return string

    def get_specific_print(self, key, value):
        """Print a subset of the checkbook

        Parameters:
            key (string) : the key to to get the subset from
            value (int | string) : the value from key to get
        """
        string = self._gen_header_print()
        string += ROW_SEP
        string += self._gen_trans_print(self._get_specific_list(key, value))
        return string

    def _get_specific_list(self, key, value):
        """Gets the subset list based on the given input

        Parameters:
            key (string) : the key to to get the subset from
            value (int | string) : the value from key to get
        """
        func = self.specific_print_functions[key.capitalize()]

        if value.isdigit():
            func_param = int(value)
        else:
            func_param = value.capitalize()

        return_list = func(self, func_param)

        return return_list

    def __str__(self):
        """A string representation of a checkbook"""
        string = self._gen_header_print()
        string += ROW_SEP
        string += self._gen_trans_print()
        string += self._gen_total_line_print()
        string += ROW_SEP
        return string

    specific_print_functions = {
        "Date": get_month,
        "Trans": get_transaction_type,
        "Category": get_category
    }
