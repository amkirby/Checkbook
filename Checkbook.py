#********************************************************************
# File    : Checkbook.py
# Date    : 9/2/2015
# Author  : Allen Kirby
# Purpose : A class that represents a checkbook
#********************************************************************

import CheckbookTransaction as CBT
import xml.etree.ElementTree as ET
from Constants import printConstants as PC
from Constants import config
import locale
from datetime import datetime
import XMLProcessor as XML

ROW_SEP = '\n' + (PC.HLINE_CHAR * (sum(PC.SIZELIST) + len(PC.SIZELIST))) + '\n'

class Checkbook:
    """A class that represents a checkbook
    Attributes:
        checkRegister (list) : contains instances of CheckbookTransaction
    """
    def __init__(self):
        """Initializes an empty check register"""
        self.checkRegister = []
        self.fileName = config.FILE_NAME
        self.edited = False

    def add(self, cbtList):
        """Adds the specified list to the checkbook
        Parameter:
            cbtList (list) : contains values in the order of the CBT.KEYS that
                             are used to create a transaction
        """
        cbt = CBT.CheckbookTransaction()
        for i in range(len(cbtList)):
            cbt.setValue(CBT.KEYS[i], cbtList[i])
        self.checkRegister.append(cbt)
        self.edited = True

    def addSingleTrans(self, cbt):
        """Adds a CheckbookTransaction to the register
        Parameter:
             cbt (CheckbookTransaction) : the CBT to be added to the checkbook
        """
        self.checkRegister.append(cbt)
        self.edited = True

    def load(self, fileName):
        """Tries to load the specified file name into the check register
        Parameter:
            fileName (string) : the file to load into the checkbook
        """
        self.fileName = fileName
        if not config.USE_SQL:
            self.checkRegister = XML.XMLProcessor.load(self.fileName)

    def clear(self):
        """Clears the checkbook"""
        del self.checkRegister[:]
        CBT.CheckbookTransaction.resetUID()

    def save(self):
        """Saves the checkbook in XML format"""
        if not config.USE_SQL:
            XML.XMLProcessor.save(self.fileName, self.checkRegister)
        self.edited = False

    def isEdited(self):
        """Returns if the checkbook has been edited"""
        return (self.edited)

    def setEdited(self, edit):
        """Sets the edited status to the specified value
        Parameter:
            edit (boolean) : the state to set if the checkbook is edited
        """
        self.edited = edit

    def getTransactionType(self, transType):
        """Gets all transactions with the specified trans type
        Parameter:
            transType (string) : the transaction type to gather
        """
        returnList = []
        for elem in self.checkRegister:
            if(elem.getDictionary().get("Trans") == transType):
                returnList.append(elem)
        return (returnList)

    def getCategory(self, cat):
        """Gets all transactions with the specified category
        Parameter:
            cat (string) : the category to gather
        """
        returnList = []
        for elem in self.checkRegister:
            if(elem.getDictionary().get("Category") == cat):
                returnList.append(elem)
        return (returnList)

    def getMonth(self, findMonth):
        """Gets all transactions with the specified month
        Parameter:
            findMonth (int) : the integer value for the month to gather
        """
        month = findMonth
        if type(month) is not int:
            month = int(month)

        returnList = []
        for elem in self.checkRegister:
            date = elem.getDictionary().get("Date")
            if(date.month == month):
                returnList.append(elem)
        return (returnList)

    def getTotalForTrans(self, trans):
        """Get the total amount for the specified trans type
        Parameter:
            trans (string) : the transaction type that is totaled
        """
        transList = self.getTransactionType(trans)
        total = 0.0
        for elem in transList:
            total += elem.getAmount()
        return total

    def getTotalForTransMonth(self, trans, month):
        """Get the total for the specified transaction in the specified month
        Parameters:
            trans (string) : the transaction type to total
            month (int)    : the month to total the trans type
        """
        monthList = self.getMonth(month)
        total = 0.0
        for elem in monthList:
            if elem.getValue("Trans") == trans:
                total += elem.getAmount()
        return (total)

    def getTotalForCat(self, category):
        """Get the total for the specified category
        Parameter:
            category (string) : The category to total
        """
        catList = self.getCategory(category)
        total = 0.0
        for elem in catList:
            total += elem.getAmount()
        return total

    def getTotalForCatMonth(self, cat, month):
        """Get the total for the specified transaction in the specified month
        Parameters:
            cat (string) : the category to total
            month (int)  : the month to total the trans type
        """
        monthList = self.getMonth(month)
        total = 0.0
        for elem in monthList:
            if elem.getValue("Category") == cat:
                total += elem.getAmount()
        return (total)

    def getTotal(self):
        """Gets the total for the register"""
        total = 0.0
        for elem in self.checkRegister:
            total += elem.getAmount()
        return total

    def getMonthTotal(self, month):
        """Gets the total for the specified month
        Parameter:
            month (int) : the month to total
        """
        monthList = self.getMonth(month)
        total = 0.0
        for elem in monthList:
            total += elem.getAmount()
        return (total)

    def findTransaction(self, inTrans):
        """Gets the specified transaction number from the register
        Parameter:
            inTrans (int) : the transaction to gather
        """
        return self.checkRegister[inTrans - 1]

    def _genTotalLinePrint(self):
        """creates the total line at the bottom of the register"""
        string = PC.VLINE_CHAR
        # format total: text
        formatString = '{:>' + str(sum(PC.SIZELIST[:-2]) + 4) + '}'
        string += formatString.format("Total : ")
        # format amount
        formatString = '{:^' + str((PC.SIZELIST[-2])) + '}'
        string += formatString.format(locale.currency(self.getTotal(), grouping=config.THOUSAND_SEP))
        # format final bar
        formatString = '{:>' + str((PC.SIZELIST[-1]) + 2) + '}'
        string += formatString.format(PC.VLINE_CHAR)
        return (string)

    def _genHeaderPrint(self):
        """Creates the header line at the top of the register"""
        header = ROW_SEP
        header += PC.VLINE_CHAR
        for i in range(len(CBT.KEYS)):
            headerLength = PC.SIZELIST[i]
            formatString = '{:^' + str(headerLength) + '}'
            header += formatString.format(CBT.KEYS[i]) + PC.VLINE_CHAR
        return (header)

    def _genTransPrint(self, printList=None):
        """Creates the print for each transaction in the register
        Parameter:
            printList (list) : the list of CBTs to loop through to generate
                               the transaction print. If None, loop through 
                               the whole checkbook
        """
        iterList = printList
        if (iterList is None):
            iterList = self.checkRegister

        string = ''
        for elem in iterList:
            string += str(elem)
            string += ROW_SEP
        return (string)
        
    def getSpecificPrint(self, key, value):
        """Print a subset of the checkbook
        Parameters:
            key (string) : the key to to get the subset from
            value (int | string) : the value from key to get
        """
        string = self._genHeaderPrint()
        string += ROW_SEP
        string += self._genTransPrint(self._getSpecificList(key, value))
        return string

    def _getSpecificList(self, key, value):
        """Gets the subset list based on the given input
        Parameters:
            key (string) : the key to to get the subset from
            value (int | string) : the value from key to get
        """
        func = self.specific_print_functions[key.capitalize()]

        if value.isdigit():
            funcParam = int(value)
        else:
            funcParam = value.capitalize()

        returnList = func(self, funcParam)

        return returnList

    def __str__(self):
        """A string representation of a checkbook"""
        string = self._genHeaderPrint()
        string += ROW_SEP
        string += self._genTransPrint()
        string += self._genTotalLinePrint() 
        string +=  ROW_SEP
        return (string)

    specific_print_functions = {
        "Date" : getMonth,
        "Trans" : getTransactionType,
        "Category" : getCategory
    }
