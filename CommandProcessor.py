#*********************************************************************
# File: CommandProcessor.py
# Author: Allen Kirby
# Date : 10/09/2015
# Purpose: process the commands entered by the user
#*********************************************************************

import Checkbook as CB
import CheckbookTransaction as CBT
import checkbookReport as CR
from Constants import config
from Constants import commands

class CommandProcessor:
    """A class to process commands entered by the user
    Attributes:
        checkbook (Checkbook) : the current checkbook the user is using
    """
    def __init__(self, checkbook):
        """Initializes the checkbook that will be used for the operations"""
        self.checkbook = checkbook

    def _doSave(self):
        """Saves the checkbook"""
        save = input("Would you like to save? (y or n) ")
        if(save.lower() == "y"):
            self.checkbook.save()
            print("save successful!")

    def processAddCommand(self):
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
        self.checkbook.addSingleTrans(cbt)

    def processEditCommand(self):
        """Edit a transaction"""
        editTrans = int(input("Which transaction do you want to edit? : "))
        trans = self.checkbook.findTransaction(editTrans)
        for key in CBT.KEYS:
            if key != "Num":
                if key == "Category":
                    print("Categories to choose:")
                    for cat in config.CATEGORIES:
                        print("  " + cat)
                val = input(key + " (" + str(trans.getValue(key)) + ")" + " : ")
                if(val.strip() != ""):
                    trans.setValue(key, val.capitalize())
                    self.checkbook.setEdited(True)

    def processReportCommand(self):
        """Generate a report"""
        print("Report Types:")
        for elem in CR.REPORT_TYPES:
            print("  ", elem)
        repType = input("Enter desired report : ")
        cr = CR.CheckbookReport(self.checkbook)
        if(repType.capitalize() == "Monthly"):
            month = int(input("Enter desired month as a number : "))
            cr.genMonthlyReport(month)
        elif(repType.capitalize() == "Total"):
            cr.genReport()

    #TODO: should it return checkbook?
    def processLoadCommand(self):
        """Load another checkbook"""
        if(self.checkbook.isEdited()):
            self._doSave()

        fileName = input("Enter an XML file to load : ")
        self.checkbook = CB.Checkbook()
        self.checkbook.load(fileName)

    def processSaveCommand(self):
        """Save the checkbook"""
        if(self.checkbook.isEdited()):
            self._doSave()

    def processHelpCommand(self):
        """Prints the help text"""
        print(commands.HELP_TEXT)

    def processPrintCommand(self):
        """Prints the checkbook"""
        print(self.checkbook)
