#********************************************************************
# File    : CheckbookTransaction.py
# Date    : 9/2/2015
# Author  : Allen Kirby
# Purpose : A class that represents a Checkbook Transaction.
#           Contains the date, the trans type, a desc, the amount,
#           and the current transaction number
#********************************************************************

from Constants import printConstants as PC
from Constants import config
from datetime import datetime
import locale
locale.setlocale(config.LOCALE, '') # set the locale for printing the amount

# the Keys used for the Transaction and printing the transaction
KEYS = ["Date", "Trans", "Category", "Desc", "Amount", "Num"]

class CheckbookTransaction:
    """This class represents a Checkbook Transaction
    Class Variables:
        UID : an identifier for the transaction
    Attributes:
        data : a dictionary to contain the transaction
    """
    _UID = 1 # The current transaction number
    
    def __init__(self):
        """Creates an empty transaction with the next available UID"""
        self.data = dict()
        for elem in KEYS:
            self.data[elem] = None
        self.data[KEYS[-1]] = CheckbookTransaction._UID
        CheckbookTransaction._UID += 1
        
    def getItems(self):
        """Gets the key, value of the transaction"""
        return dict.items(self.data)

    def getDictionary(self):
        """Gets the data as a dictionary"""
        return self.data

    def getAmount(self):
        """Gets the amount of the transaction"""
        return self.data.get("Amount")

    def getValue(self, key):
        """Gets the value of the specified key"""
        return self.data.get(key)

    def getDate(self):
        return self.data.get("Date")

    def setValue(self, key, value):
        """Sets the specified key with the specified value"""
        insertVal = value
        if(key == "Date"):
            insertVal = datetime.strptime(value, config.DATE_FORMAT).date()
        elif(key == "Amount"):
            insertVal = float(value)
        self.data[key] = insertVal

    def __str__(self):
        """A string representation of a Checkbook Transaction"""
        string = PC.VLINE_CHAR
        for i in range(len(KEYS)):
            headerLength = PC.SIZELIST[i]
            formatString = '{:^' + str(headerLength) + '}'
            val = self.data.get(KEYS[i])
            if type(val) is datetime:
                val = datetime.strftime(self.data.get(KEYS[i]), config.DATE_FORMAT)
            elif type(val) is float:
                val = locale.currency(val, grouping=config.THOUSAND_SEP)
            string += formatString.format(str(val)) + PC.VLINE_CHAR
        return string

