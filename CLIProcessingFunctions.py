from Constants import commands
from Constants import config
import Checkbook as CB
import CheckbookTransaction as CBT
import checkbookReport as CR
import CommandProcessor as CP
import CLIProcessingFunctions as CPF

def _doSave(checkbook):
    """Saves the checkbook"""
    save = input("Would you like to save? (y or n) ")
    if(save.lower() == "y"):
        checkbook.save()
        print("save successful!")

def processAddCommand(checkbook):
    """Adds a transaction to the checkbook"""
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

def processEditCommand(checkbook):
    """Edit a transaction"""
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

def processReportCommand(checkbook):
    """Generate a report"""
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

def processLoadCommand(checkbook):
    """Load another checkbook"""
    if(checkbook.isEdited()):
        _doSave()

    fileName = input("Enter an XML file to load : ")
    checkbook.clear()
    checkbook.load(fileName)

def processSaveCommand(checkbook):
    """Save the checkbook"""
    if(checkbook.isEdited()):
        _doSave(checkbook)

def processHelpCommand(checkbook):
    """Prints the help text"""
    print(commands.HELP_TEXT)

def processPrintCommand(checkbook):
    """Prints the checkbook"""
    print(checkbook)
