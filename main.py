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

checkbook = CB.Checkbook()
checkbook.load(config.FILE_NAME)
commProcessor = CP.CommandProcessor(checkbook)
                
if __name__ == "__main__":
    print("Welcome to your checkbook!")
    commProcessor.processPrintCommand()
    val = input("What would you like to do? : ").lower()

    while(val not in commands.EXIT_LIST):
        if(val == commands.HELP_COMMAND):
            commProcessor.processHelpCommand()
        elif(val == commands.PRINT_COMMAND):
            commProcessor.processPrintCommand()
        elif(val == commands.ADD_COMMAND):
            commProcessor.processAddCommand()
        elif(val == commands.EDIT_COMMAND):
            commProcessor.processEditCommand()
        elif(val == commands.REPORT_COMMAND):
            commProcessor.processReportCommand()
        elif(val == commands.LOAD_COMMAND):
            commProcessor.processLoadCommand()
        elif(val == commands.SAVE_COMMAND):
            commProcessor.processSaveCommand()
            
        commProcessor.processPrintCommand()

        val = input("What would you like to do? : ").lower()

    # Save prompt
    if(checkbook.isEdited()):
        commProcessor.processSaveCommand()
