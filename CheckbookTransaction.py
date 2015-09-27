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
    
    # def __init__(self, date, transType, desc, amount):
    #     """Initializes the Checkbook Transaction
    #     Paramaters:
    #         date (string)      : the date the transaction occurred (converted to datetime)
    #         transType (string) : the trans type, either Credit or Debit
    #         desc (string)      : a description for the transaction
    #         amount (string)    : the amount of the transaction (converted to float)
    #     """
    #     # TODO: make more generic
    #     self.data = {KEYS[0]: datetime.strptime(date, config.DATE_FORMAT), KEYS[1]: transType, KEYS[2]: desc,
    #                  KEYS[3]: float(amount), KEYS[4]: CheckbookTransaction._UID}
    #     CheckbookTransaction._UID += 1

    def __init__(self):
        self.data = dict()
        for elem in KEYS:
            self.data[elem] = None
        self.data[KEYS[-1]] = CheckbookTransaction._UID
        CheckbookTransaction._UID += 1
        
    def getItems(self):
        return dict.items(self.data)

    def getDictionary(self):
        return self.data

    def getAmount(self):
        return self.data.get("Amount")

    def getValue(self, key):
        return self.data.get(key)

    def setValue(self, key, value):
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

