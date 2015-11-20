from Constants import commands
from Constants import config
import Checkbook as CB
import CheckbookTransaction as CBT
import checkbookReport as CR

def _doSave(checkbook):
    """Saves the checkbook"""
    save = input("Would you like to save? (y or n) ")
    if(save.lower() == "y"):
        checkbook.save()
        print("save successful!")

def _selectWithNumber(textList, prompt, key, defText = None):
    """Select a value from the given list by using it's index
    Parameters:
        textList (list) : a list of strings to Select
        prompt (str)    : a header for selection
        key (str)       : a prompt for input
        defText (str)   : default text to display
    Returns:
        (str) : the chosen value from the given list
    """
    maxLen = len(max(textList, key=len))
    formatString = "{:<" + str(maxLen) + "}"
    prevText = ""
    if defText is not None:
        prevText = "(" + str(defText) + ")"

    for i in range(len(textList)):
        print("  " + formatString.format(textList[i]), i)
    val = input(key + prevText + " : ")
    if val.strip() != "" and val.isdigit():
        val = textList[int(val)]
    return val

def processAddCommand(checkbook):
    """Adds a transaction to the checkbook"""
    print("Enter your transaction")
    cbt = CBT.CheckbookTransaction()
    for key in CBT.KEYS:
        if key != "Num":
            if key == "Category":
                val = _selectWithNumber(config.CATEGORIES, "Categories to choose:", key)
            elif key == "Trans":
                val = _selectWithNumber(commands.TRANS_TYPES, "Transaction Types:", key)
            else:
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
                val = _selectWithNumber(config.CATEGORIES, "Categories to choose:", 
                    key, trans.getValue(key))
            elif key == "Trans":
                val = _selectWithNumber(commands.TRANS_TYPES, "Transaction Types:", 
                    key, trans.getValue(key))
            else:
                val = input(key + " (" + str(trans.getValue(key)) + ")" + " : ")
            if(val.strip() != ""):
                trans.setValue(key, val.capitalize())
                checkbook.setEdited(True)

def processReportCommand(checkbook):
    """Generate a report"""
    formatString = "{:<8}"
    print("Report Types:")
    for i in range(len(CR.REPORT_TYPES)):
        print(formatString.format(CR.REPORT_TYPES[i]), ":", i)
    repType = int(input("Enter desired report number : "))
    cr = CR.CheckbookReport(checkbook)
    repMethod = CR.CheckbookReport.dispatcher[CR.REPORT_TYPES[repType]]
    if(repType == 0):
        month = int(input("Enter desired month as a number : "))
        reportText = repMethod(cr, month)
    else:
        reportText = repMethod(cr)
    print(reportText)

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
