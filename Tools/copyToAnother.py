from typing import List

import Checkbook as CB
import CheckbookTransaction as CT
import ConfigurationProcessor as Conf
import CommandProcessor
from DataProcessors import XMLProcessor as XML
from DisplayProcessors import CLIDisplayProcessor as CDP

conf = Conf.ConfigurationProcessor()

def copy(from_book : str = "", to_book : str = ""):
    save_function = XML.XMLProcessor.save
    load_function = XML.XMLProcessor.load

    from_default_text : str = ""
    if(from_book != ""):
        from_default_text = "(" + from_book + ")"

    to_default_text : str = ""
    if(to_book != ""):
        to_default_text = "(" + to_book + ")"
    
    from_checkbook_name = input("Checkbook to copy from " + from_default_text + ": ")
    to_checkbook_name = input("Checkbook to copy to " + to_default_text + ": ")

    if(from_checkbook_name.strip() == ""):
        from_checkbook_name = from_book

    if(to_checkbook_name.strip() == ""):
        to_checkbook_name = to_book

    from_checkbook = CB.Checkbook()
    from_checkbook.load(from_checkbook_name, load_function)

    to_checkbook = CB.Checkbook()
    to_checkbook.load(to_checkbook_name, load_function)

    display_processor = CDP.CLIDisplayProcessor()
    to_command_processor = CommandProcessor.CommandProcessor(to_checkbook, display_processor)

    last_trans_of_to = to_checkbook.get_register()[-1]

    # COPY LOGIC
    reversed_from_checkbook = from_checkbook.get_register()[::-1]
    trans_to_add : List[CT.CheckbookTransaction] = []
    for current_trans in reversed_from_checkbook:
        if(current_trans != last_trans_of_to):
            trans_to_add.append(current_trans)
        else:
            break
    
    
    display_processor.print_list_of_trans(" Transactions Being Added ", conf.get_property("MAX_WIDTH"), conf.get_property("TRANS_FILL_CHAR"), trans_to_add[::-1])
    if(len(trans_to_add) > 0 and to_command_processor.confirm_selection("copy")):
        for current_trans in trans_to_add[::-1]:
            to_checkbook.add_single_trans(current_trans)

        to_command_processor.process_resequence_command(to_checkbook)
        to_command_processor.process_save_command(save_function)


def qt_copy(from_book : str = "", to_book : str = ""):
    pass