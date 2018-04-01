import locale

import CheckbookTransaction as CBT
from Constants import config
from Constants import printConstants as PC

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


def _gen_trans_print(transaction_list):
    """
    Creates the print for each transaction in the register

    @param transaction_list: the list of CBTs to loop through to generate
                             the transaction print. If None, loop through
                             the whole checkbook
    @return: pretty print for the given transaction list
    """
    string = ''
    for elem in transaction_list:
        string += str(elem)
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
    output += _gen_trans_print(transaction_list)
    output += _gen_total_line_print(total)
    output += ROW_SEP

    return output
