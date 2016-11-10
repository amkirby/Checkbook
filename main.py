#********************************************************************
# File    : main.py
# Date    : Sept. 2, 2015
# Author  : Allen Kirby
# Purpose : A checkbook program
#********************************************************************

from Constants import commands
from Constants import config
import Checkbook as CB
import CheckbookTransaction as CBT
import checkbookReport as CR
import CommandProcessor as CP
import SQLProcessor as SCP
import CLIProcessingFunctions as CPF
import XMLProcessor as XML

checkbook = CB.Checkbook()
if config.USE_SQL:
    save_function = SCP.SQLProcessor.save
    load_function = SCP.SQLProcessor.load
else:
    save_function = XML.XMLProcessor.save
    load_function = XML.XMLProcessor.load

checkbook.load(config.FILE_NAME, load_function)
commProcessor = CP.CommandProcessor(checkbook)

def _handle_input():
    """Gather user input. If the input is empty, make it an empty string.
    Returns:
        inputVal (list) : list containing one or more strings
    """
    inputVal = input("What would you like to do? : ").strip().split()
    if len(inputVal) == 0:
        inputVal = [""]

    inputVal[0].lower()
    return inputVal
                
if __name__ == "__main__":
    print("Welcome to your checkbook!")
    commProcessor.process_print_command()
    quit = False
    while(not quit):
        val = _handle_input()
        if(val[0] == commands.HELP_COMMAND):
            commProcessor.process_help_command()
        elif(val[0] == commands.PRINT_COMMAND):
            commProcessor.process_print_command(*val[1:])
        elif(val[0] == commands.ADD_COMMAND):
            commProcessor.process_add_command()
        elif(val[0] == commands.EDIT_COMMAND):
            commProcessor.process_edit_command(*val[1:])
        elif(val[0] == commands.REPORT_COMMAND):
            commProcessor.process_report_command()
        elif(val[0] == commands.LOAD_COMMAND):
            commProcessor.process_load_command(save_function, load_function, *val[1:])
            commProcessor.process_print_command()
        elif(val[0] == commands.SAVE_COMMAND):
            commProcessor.process_save_command(save_function)
        elif(val[0] in commands.EXIT_LIST):
            commProcessor.process_quit_command(save_function)
            quit = True
