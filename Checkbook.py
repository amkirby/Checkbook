#********************************************************************
# File    : Checkbook.py
# Date    : 9/2/2015
# Author  : Allen Kirby
# Purpose : A class that represents a checkbook
#********************************************************************

import CheckbookTransaction as CT
import xml.etree.ElementTree as ET
from Constants import printConstants as PC
from Constants import config
import locale
from datetime import datetime

ROW_SEP = '\n' + (PC.HLINE_CHAR * (sum(PC.SIZELIST) + len(PC.SIZELIST))) + '\n'

class Checkbook:
    """A class that represents a checkbook
    Attributes:
        checkRegister (list) : contains instances of CheckbookTransaction
    """
    def __init__(self):
        """Initializes an empty check register"""
        self.checkRegister = []

    def add(self, cbtList):
        """Adds the specified list to the checkbook"""
        cbt = CT.CheckbookTransaction()
        for i in range(len(cbtList)):
            cbt.setValue(CT.KEYS[i], cbtList[i])
        self.checkRegister.append(cbt)

    def addSingleTrans(self, cbt):
        self.checkRegister.append(cbt)

    def load(self, fileName):
        """Tries to load the specified file name into the check register"""
        try:
            root = ET.parse(fileName)
            treeIter = root.iter("Transaction")
            for elem in treeIter:
                cbt = CT.CheckbookTransaction()
                for child in list(elem):
                    cbt.setValue(child.tag, child.text)
                self.checkRegister.append(cbt)
        except FileNotFoundError:
            print("A new file will be created when you save")
        
        

    def save(self):
        """Saves the checkbook"""
        root = ET.Element('Transactions')
        for elem in self.checkRegister:
            currTrans = ET.SubElement(root, "Transaction")
            for key, value in elem.getItems():
                transElem = ET.SubElement(currTrans, key)
                if(key == "Date"):
                    value = datetime.strftime(value, config.DATE_FORMAT)
                transElem.text = str(value)
        tree = ET.ElementTree(root)
        tree.write(config.FILE_NAME, xml_declaration=True)

    def getTransactionType(self, transType):
        returnList = []
        for elem in self.checkRegister:
            if(elem.getDictionary().get("Trans") == transType):
                returnList.append(elem)
        return (returnList)

    def getTotal(self):
        total = 0.0
        for elem in self.checkRegister:
            total += elem.getAmount()
        return total

    def _genTotalLinePrint(self):
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
        header = ROW_SEP
        header += PC.VLINE_CHAR
        for i in range(len(CT.KEYS)):
            headerLength = PC.SIZELIST[i]
            formatString = '{:^' + str(headerLength) + '}'
            header += formatString.format(CT.KEYS[i]) + PC.VLINE_CHAR
        return (header)

    def _genTransPrint(self):
        string = ''
        for elem in self.checkRegister:
            string += str(elem)
            string += ROW_SEP
        return (string)
        
        
    def __str__(self):
        """A string representation of a checkbook"""
        string = self._genHeaderPrint()
        string += ROW_SEP
        string += self._genTransPrint()
        string += self._genTotalLinePrint() 
        string +=  ROW_SEP
        return (string)

