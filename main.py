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
import CLIProcessingFunctions as CPF

checkbook = CB.Checkbook()
checkbook.load(config.FILE_NAME)
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
    commProcessor.processPrintCommand()
    val = _handle_input()
    while(val[0] not in commands.EXIT_LIST):
        if(val[0] == commands.HELP_COMMAND):
            commProcessor.processHelpCommand()
        elif(val[0] == commands.PRINT_COMMAND):
            commProcessor.processPrintCommand(*val[1:])
        elif(val[0] == commands.ADD_COMMAND):
            commProcessor.processAddCommand()
        elif(val[0] == commands.EDIT_COMMAND):
            commProcessor.processEditCommand(*val[1:])
        elif(val[0] == commands.REPORT_COMMAND):
            commProcessor.processReportCommand()
        elif(val[0] == commands.LOAD_COMMAND):
            commProcessor.processLoadCommand(*val[1:])
            commProcessor.processPrintCommand()
        elif(val[0] == commands.SAVE_COMMAND):
            commProcessor.processSaveCommand()

        val = _handle_input()

    # Save prompt
    if(commProcessor.checkbook.isEdited()):
        commProcessor.processSaveCommand()
