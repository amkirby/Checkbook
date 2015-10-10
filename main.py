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
checkbook = CB.Checkbook()
checkbook.load(config.FILE_NAME)

def _doSave():
    """Saves the checkbook"""
    save = input("Would you like to save? (y or n) ")
    if(save.lower() == "y"):
        checkbook.save()
        print("save successful!")

def _processAddCommand():
    print("Enter your transaction")
    cbt = CBT.CheckbookTransaction()
    for key in CBT.KEYS:
        if key != "Num":
            if key == "Category":
                print("Categories to choose:")
                for cat in config.CATEGORIES:
                    print("  " + cat)
            val = input(key + " : ")
            cbt.setValue(key, val.capitalize())
    checkbook.addSingleTrans(cbt)

def _processEditCommand():
    editTrans = int(input("Which transaction do you want to edit? : "))
    trans = checkbook.findTransaction(editTrans)
    for key in CBT.KEYS:
        if key != "Num":
            if key == "Category":
                print("Categories to choose:")
                for cat in config.CATEGORIES:
                    print("  " + cat)
            val = input(key + " (" + str(trans.getValue(key)) + ")" + " : ")
            if(val.strip() != ""):
                trans.setValue(key, val.capitalize())
                checkbook.setEdited(True)

def _processReportCommand():                
    print("Report Types:")
    for elem in CR.REPORT_TYPES:
        print("  ", elem)
    repType = input("Enter desired report : ")
    cr = CR.CheckbookReport(checkbook)
    if(repType.capitalize() == "Monthly"):
        month = int(input("Enter desired month as a number : "))
        cr.genMonthlyReport(month)
    elif(repType.capitalize() == "Total"):
        cr.genReport()

def _processLoadCommand():
    if(checkbook.isEdited()):
        _doSave()
        cbEdited = False

    fileName = input("Enter an XML file to load : ")
    checkbook = CB.Checkbook()
    checkbook.load(fileName)

def _processSaveCommand():
    if(checkbook.isEdited()):
        _doSave()

def _processHelpCommand():        
    print(commands.HELP_TEXT)
                
if __name__ == "__main__":
    print("Welcome to your checkbook!")
    print(checkbook)
    val = input("What would you like to do? : ").lower()

    while(val not in commands.EXIT_LIST):
        if(val == commands.HELP_COMMAND):
            _processHelpCommand()
        elif(val == commands.PRINT_COMMAND):
            print(checkbook)
        elif(val == commands.ADD_COMMAND):
            _processAddCommand()
        elif(val == commands.EDIT_COMMAND):
            _processEditCommand()
        elif(val == commands.REPORT_COMMAND):
            _processReportCommand()
        elif(val == commands.LOAD_COMMAND):
            _processLoadCommand()
        elif(val == commands.SAVE_COMMAND):
            _processSaveCommand()
            
        print(checkbook)

        val = input("What would you like to do? : ").lower()

    # Save prompt
    if(checkbook.isEdited()):
        _doSave()
