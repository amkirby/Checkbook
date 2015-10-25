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
                
if __name__ == "__main__":
    print("Welcome to your checkbook!")
    commProcessor.processPrintCommand()
    val = input("What would you like to do? : ").lower().strip()

    while(val not in commands.EXIT_LIST):
        if(val == commands.HELP_COMMAND):
            commProcessor.processCommand(CPF.processHelpCommand)
        elif(val == commands.PRINT_COMMAND):
            commProcessor.processCommand(CPF.processPrintCommand)
        elif(val == commands.ADD_COMMAND):
            commProcessor.processCommand(CPF.processAddCommand)
        elif(val == commands.EDIT_COMMAND):
            commProcessor.processCommand(CPF.processEditCommand)
        elif(val == commands.REPORT_COMMAND):
            commProcessor.processCommand(CPF.processReportCommand)
        elif(val == commands.LOAD_COMMAND):
            commProcessor.processCommand(CPF.processLoadCommand)
            commProcessor.processCommand(CPF.processPrintCommand)
        elif(val == commands.SAVE_COMMAND):
            commProcessor.processCommand(CPF.processSaveCommand)

        val = input("What would you like to do? : ").lower().strip()

    # Save prompt
    if(commProcessor.checkbook.isEdited()):
        commProcessor.processCommand(CPF.processSaveCommand)
