#*********************************************************************
# File: CommandProcessor.py
# Author: Allen Kirby
# Date : 10/09/2015
# Purpose: process the commands entered by the user
#*********************************************************************

from Constants import config
from Constants import commands
import Checkbook as CB
import CheckbookTransaction as CBT
import checkbookReport as CR
import XMLProcessor as XML


class CommandProcessor:
    """A class to process commands entered by the user. A function should be
    passed to each method to do the actual processing.
    ****NOTE: Each passed function is expected to take a Checkbook object as a parameter.
    ****NOTE: The separate methods remain to facilitate inheritance if desired.
    Attributes:
        checkbook (Checkbook) : the current checkbook the user is using
    """
    def __init__(self, checkbook):
        """Initializes the checkbook that will be used for the operations
        Parameter:
            checkbook (Checkbook) : the checkbook to operate on
        """
        self.checkbook = checkbook

    def processCommand(self, function, *args):
        """Performs the effects of the specified function on the checkbook
        Parameter:
            function (function) : A function that takes a checkbook and performs
                                  some action
            args (variable args) : optional arguments that can be passed to the specified
                                   function
        """
        function(self.checkbook, *args)

    def _doSave(self, save_function):
        """Saves the checkbook"""
        save = input("Would you like to save? (y or n) ")
        if(save.lower() == "y"):
            self.checkbook.save(save_function)
            print("save successful!")

    def _selectWithNumber(self, textList, prompt, key, defText = None):
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
        if val.strip() != "" and val.isdigit() and (int(val) >= 0 and int(val) < len(textList)):
            val = textList[int(val)]
        return val

    def processAddCommand(self):
        """Adds a transaction to the checkbook"""
        print("Enter your transaction")
        cbt = CBT.CheckbookTransaction()
        for key in CBT.KEYS:
            if key != "Num":
                if key == "Category":
                    val = self._selectWithNumber(config.CATEGORIES, "Categories to choose:", key)
                elif key == "Trans":
                    val = self._selectWithNumber(commands.TRANS_TYPES, "Transaction Types:", key)
                else:
                    val = input(key + " : ")

                cbt.setValue(key, val.capitalize())
        self.checkbook.addSingleTrans(cbt)

    def processEditCommand(self, *args):
        """Edit a transaction"""
        if not args:
            editTrans = int(input("Which transaction do you want to edit? : "))
        else:
            editTrans = int(args[0])

        trans = self.checkbook.findTransaction(editTrans)
        for key in CBT.KEYS:
            if key != "Num":
                if key == "Category":
                    val = self._selectWithNumber(config.CATEGORIES, "Categories to choose:", 
                        key, trans.getValue(key))
                elif key == "Trans":
                    val = self._selectWithNumber(commands.TRANS_TYPES, "Transaction Types:", 
                        key, trans.getValue(key))
                else:
                    val = input(key + " (" + str(trans.getValue(key)) + ")" + " : ")
                if(val.strip() != ""):
                    trans.setValue(key, val.capitalize())
                    self.checkbook.setEdited(True)

    def processReportCommand(self):
        """Generate a report"""
        formatString = "{:<8}"
        month = None
        print("Report Types:")
        for i in range(len(CR.REPORT_TYPES)):
            print(formatString.format(CR.REPORT_TYPES[i]), ":", i)
        repType = int(input("Enter desired report number : "))
        cr = CR.CheckbookReport(self.checkbook)
        repMethod = CR.CheckbookReport.dispatcher[CR.REPORT_TYPES[repType]]
        if(repType == 0):
            month = int(input("Enter desired month as a number : "))

        reportText = repMethod(cr, month)
        print(reportText)

    def processLoadCommand(self, save_function, load_function, *args):
        """Load another checkbook"""
        if(self.checkbook.isEdited()):
            self._doSave(save_function)

        if not args:
            fileName = input("Enter an XML file to load : ")
        else:
            fileName = args[0]
        self.checkbook.clear()
        self.checkbook.load(fileName, load_function)

    def processSaveCommand(self, save_function):
        """Save the checkbook"""
        if(self.checkbook.isEdited()):
            self._doSave(save_function)

    def processHelpCommand(self):
        """Prints the help text"""
        print(commands.HELP_TEXT)

    def processPrintCommand(self, *args):
        """Prints the checkbook"""
        if not args:
            print(self.checkbook)
        elif (len(args) == 2):
            print(self.checkbook.getSpecificPrint(*args))
        else:
            printHelpText = """
Usage : print [<key> <value> | <help>]
Possible keys with their values :
    Date     : a number to represent the month
    Trans    : {}
    Category : {}
help displays this text
            """
            print (printHelpText.format(", ".join(s for s in commands.TRANS_TYPES), ", ".join(s for s in config.CATEGORIES)))
